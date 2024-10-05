vim.g.mapleader = " "

-- Note: Plugin specific keymaps are to be found at the respective
-- section in lazy.lua

-- Creating new buffers
vim.keymap.set("n", "<leader>wh", vim.cmd.new)
vim.keymap.set("n", "<leader>wv", vim.cmd.vne)

-- Navigating between buffers
vim.keymap.set("n", "<leader><left>", function()
    vim.cmd("wincmd h")
end)
vim.keymap.set("n", "<leader><down>", function()
    vim.cmd("wincmd j")
end)
vim.keymap.set("n", "<leader><up>", function()
    vim.cmd("wincmd k")
end)
vim.keymap.set("n", "<leader><right>", function()
    vim.cmd("wincmd l")
end)
