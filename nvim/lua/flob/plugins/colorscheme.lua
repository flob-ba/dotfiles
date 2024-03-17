return {
    { "morhetz/gruvbox", priority = 1000, config = function ()
        vim.g.gruvbox_contrast_dark = "hard"
    end },
    { "LazyVim/LazyVim", opts = { colorscheme = "gruvbox" } },
}
