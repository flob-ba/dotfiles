return {
    {
        "morhetz/gruvbox",
        lazy = false,
        priority = 1000,
        config = function ()
            vim.cmd("colorscheme gruvbox")
            vim.g.gruvbox_constrast_dark = "hard"
        end,
    }
}
