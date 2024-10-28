return {
    {'VonHeikemen/lsp-zero.nvim', branch = 'v3.x'},
    {
        'neovim/nvim-lspconfig',
        opts = function ()
            local ret = {
                diagnostics = {
                    update_in_insert = true,
                }
            }
            return ret
        end,
        config = function (_,opts)
            vim.diagnostic.config(vim.deepcopy(opts.diagnostics))
        end,
    },
}
