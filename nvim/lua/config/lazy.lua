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

-- Load plugins
require("lazy").setup("config.plugins")

require("autoclose").setup({
    keys = {
        ["$"] = { escape = true, close = true, pair = "$$", enabled_filetypes = {"tex"}},
    }
})

require("colorizer").setup({})


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
        ["clangd"] = {"h", "c", "hpp", "cpp"},
    },
})
local lsp_config = require("lspconfig")
lsp_config.clangd.setup({})
lsp_config.cmake.setup({
    filetypes = { "cmake", "CMakeLists.txt" }
})
vim.keymap.set("n", "<leader>ow", vim.diagnostic.open_float)

local telescope = require("telescope")
local telescopeBuiltin = require("telescope.builtin")
local telescopeConfig = require("telescope.config")
local vimgrepArguments = { unpack(telescopeConfig.values.vimgrep_arguments) }
table.insert(vimgrepArguments, "--hidden")
table.insert(vimgrepArguments, "--glob")
table.insert(vimgrepArguments, "!**/.git/*")
telescope.setup({
    defaults = {
        vimgrep_arguments = vimgrepArguments,
    },
    pickers = {
        find_files = {
            find_command = { "rg", "--files", "--hidden", "--glob", "!**/.git/*", },
        },
    },
})
vim.keymap.set("n", "<leader>ff", telescopeBuiltin.find_files, {})
vim.keymap.set("n", "<leader>fbs", telescopeBuiltin.lsp_document_symbols, {})
vim.keymap.set("n", "<leader>fws", telescopeBuiltin.lsp_workspace_symbols, {})

local luasnip = require("luasnip")
luasnip.config.setup({
    enable_autosnippets = true,
})
require("luasnip.loaders.from_snipmate").lazy_load()

local lsp_kind = require("lspkind")
local cmp = require("cmp")
cmp.setup({
    snippet = {
        expand = function(args)
            luasnip.lsp_expand(args.body)
        end
    },
    sources = cmp.config.sources({
        { name = "nvim_lsp" },
        { name = "luasnip" },
        { name = "vimtex" },
    }, {
        name = "buffer",
    }),
    mapping = {
        ["<Enter>"] = cmp.mapping.confirm({behavior = cmp.ConfirmBehavior.Replace, select = true }),
        ["<Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
                cmp.select_next_item()
            elseif luasnip.locally_jumpable(1) then
                luasnip.jump(1)
            else
                fallback()
            end
        end, {"i", "s"}),
        ["<S-Tab>"] = cmp.mapping(function(fallback)
            if cmp.visible() then
                cmp.select_prev_item()
            elseif luasnip.locally_jumpable(-1) then
                luasnip.jump(-1)
            else
                fallback()
            end
        end, {"i", "s"}),
    },
    formatting = {
        format = lsp_kind.cmp_format(),
    },
    view = { entries = "custom" },
    experimental = {
        ghost_text = true,
    },
})

