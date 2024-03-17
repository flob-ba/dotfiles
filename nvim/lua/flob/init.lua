vim.g.mapleader = " "

vim.cmd("set shiftwidth=4 smarttab")
vim.cmd("set expandtab")
vim.cmd("set tabstop=8 softtabstop=0")

vim.cmd("set whichwrap+=<h")
vim.cmd("set whichwrap+=>l")
vim.cmd("set whichwrap+=[,]")

vim.cmd("set number relativenumber")

vim.cmd("ino \" \"\"<left>")
vim.cmd("ino ' ''<left>")
vim.cmd("ino ( ()<left>")
vim.cmd("ino [ []<left>")
vim.cmd("ino { {}<left>")
vim.cmd("ino {<CR> {<CR>}<ESC>O")
vim.cmd("set splitbelow")
vim.cmd("set splitright")

vim.keymap.set("n", "<leader>wh", vim.cmd.new)
vim.keymap.set("n", "<leader>wv", vim.cmd.vne)

vim.opt.termguicolors = true

local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not vim.loop.fs_stat(lazypath) then
    vim.fn.system({
        "git",
        "clone",
        "--filter=blob:none",
        "https://github.com/folke/lazy.nvim.git",
        "--branch=stable",
        lazypath,
    })
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup("flob.plugins")

require("toggleterm").setup({
    open_mapping = [[<C-t>]],
    direction = "float",
    float_opts = {
        border = "curved",
    },
})

local telescope = require("telescope")
local telescopebuiltin = require("telescope.builtin")
local telescopeConfig = require("telescope.config")

local vimgrep_arguments = { unpack(telescopeConfig.values.vimgrep_arguments) }
table.insert(vimgrep_arguments, "--hidden")
table.insert(vimgrep_arguments, "--glob")
table.insert(vimgrep_arguments, "!**/.git/*")

telescope.setup({
    defaults = {
        vimgrep_arguments = vimgrep_arguments,
    },
    pickers = {
        find_files = {
            find_command = { "rg", "--files", "--hidden", "--glob", "!**/.git/*" }
        }
    }
})

vim.keymap.set("n", "<leader>ff", telescopebuiltin.find_files, {})
vim.keymap.set("n", "<leader>fbs", telescopebuiltin.lsp_document_symbols, {})
vim.keymap.set("n", "<leader>fws", telescopebuiltin.lsp_workspace_symbols, {})

require("lualine").setup()
vim.cmd("set noshowmode")

local lsp_zero = require("lsp-zero")
lsp_zero.on_attach(function(client, bufnr)
    lsp_zero.default_keymaps({ buffer = bufnr })
end)
lsp_zero.format_on_save({
    format_opts = {
        async = false,
        timeout_ms = 10000,
    },
    servers = {
        ["clangd"] = {"c", "cpp"}
    }
})

vim.diagnostic.config({ update_in_insert = true })

local cmp = require("cmp")
cmp.setup({
    snippet = {
        expand = function(args)
            vim.fn["UltiSnips#Anon"](args.body)
        end,
    },
    sources = cmp.config.sources({
        { name = "nvim_lsp" },
        { name = "ultisnips" },
        { name = "vimtex" },
    }, {
        name = "buffer",
    }),
    mapping = {
        ["<Enter>"] = cmp.mapping.confirm({behavior = cmp.ConfirmBehavior.Replace, select = true }),
        ["<Tab>"] = cmp.mapping.confirm({behavior = cmp.ConfirmBehavior.Replace, select = true }),
        ["<Escape>"] = cmp.mapping.close();
    },
    view = { entries = "custom" },
    experimental = {
        ghost_text = true,
    },
})

vim.g.UltiSnipsSnippetDirectories = {"UltiSnips", "my_snippets"}
vim.g.UltiSnipsExpandTrigger = "<s-tab>"
vim.g.UltiSnipsJumpForwardTrigger = "<tab>"
vim.g.UltiSnipsJumpBackwardTrigger = "<c-tab>"

local lspconfig = require("lspconfig");
lspconfig.lua_ls.setup({
    on_init = function(client)
        local path = client.workspace_folders[1].name
        if vim.loop.fs_stat(path .. '/.luarc.json') or vim.loop.fs_stat(path .. '/.luarc.jsonc') then
            return
        end

        client.config.settings.Lua = vim.tbl_deep_extend('force', client.config.settings.Lua, {
            runtime = {
                version = 'LuaJIT'
            },
            workspace = {
                checkThirdParty = false,
                library = {
                    vim.env.VIMRUNTIME
                }
            }
        })
    end,
    settings = {
        Lua = {}
    },
})
lspconfig.clangd.setup({
    on_new_config = function(new_config, new_cwd)
        local status, cmake = pcall(require, "cmake-tools")
        if status then
            cmake.clangd_on_new_config(new_config)
        end
    end,
})
lspconfig.cmake.setup({})
lspconfig.texlab.setup({
    settings = {
        texlab = {
            chktex = {
                onEdit = true,
                onOpenAndSave = true,
            }
        }
    }
})

require("overseer").setup({})

require("cmake-tools").setup({
    cmake_soft_link_compile_commands = false,
    cmake_compile_commands_from_lsp = true,
    cmake_executor = {
        name = "toggleterm",
    },
    cmake_runner = {
        name = "toggleterm",
    }
})

