-- Bootstrap lazy.nvim
local lazypath = vim.fn.stdpath("data") .. "/lazy/lazy.nvim"
if not (vim.uv or vim.loop).fs_stat(lazypath) then
    local lazyrepo = "https://github.com/folke/lazy.nvim.git"
    local out = vim.fn.system({ "git", "clone", "--filter=blob:none", "--branch=stable", lazyrepo, lazypath })
    if vim.v.shell_error ~= 0 then
        vim.api.nvim_echo({
            { "Failed to clone lazy.nvim:\n", "ErrorMsg" },
            { out, "WarningMsg" },
            { "\nPress any key to exit..." },
            }, true, {})
        vim.fn.getchar()
        os.exit(1)
    end
end
vim.opt.rtp:prepend(lazypath)

require("lazy").setup("flob.plugins")

-- colorscheme
vim.cmd("highlight Normal guibg=#1a1220") -- override gui background color
vim.cmd("highlight link @lsp.type.property.c cParen")
vim.cmd("highlight link @lsp.type.class.c GruvboxYellow")
vim.cmd("highlight link @lsp.type.class.cpp GruvboxYellow")
vim.cmd("highlight link @lsp.type.enum.cpp GruvboxYellow")
vim.cmd("highlight link cTypedef GruvboxOrange")
vim.cmd("highlight link cppStructure GruvboxOrange")
vim.cmd("highlight link @lsp.type.namespace.cpp GruvboxYellow")

-- lualine
require("lualine").setup()
vim.cmd("set noshowmode") -- do not show mode as lualine will do it now

-- autoclose
require("autoclose").setup()

-- lsp
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
lspconfig.cmake.setup({
    filetypes = { "cmake", "CMakeLists.txt" }
})

vim.keymap.set("n", "<leader>ow", vim.diagnostic.open_float)

-- cmp
local cmp = require("cmp")
cmp.setup({
    sources = cmp.config.sources({
        { name = "nvim_lsp" },
    }, {
        name = "buffer",
    }),
    mapping = {
        ["<Enter>"] = cmp.mapping.confirm({behavior = cmp.ConfirmBehavior.Replace, select = true }),
    },
    view = { entries = "custom" },
    experimental = {
        ghost_text = true,
    },
})

-- telescope
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
    },
})

vim.keymap.set("n", "<leader>ff", telescopebuiltin.find_files, {})
vim.keymap.set("n", "<leader>fbs", telescopebuiltin.lsp_document_symbols, {})
vim.keymap.set("n", "<leader>fws", telescopebuiltin.lsp_workspace_symbols, {})
