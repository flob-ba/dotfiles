return {
    {
        "morhetz/gruvbox",
        lazy = false,
        priority = 1000,
        config = function()
            vim.g.gruvbox_contrast_dark = "hard"
            vim.g.gruvbox_italic = 1
            vim.g.gruvbox_italicize_strings = 1
            vim.cmd("colorscheme gruvbox")
            vim.cmd("highlight link texDelimiter GruvboxYellow")
            vim.cmd("highlight link texOnlyMath GruvboxWhite")
            vim.cmd("highlight link texMathDelimBad GruvboxWhite")
        end,
    }
}
