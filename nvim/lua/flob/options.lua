local opt = vim.opt

-- Enable relative line numbering
opt.number = true
opt.relativenumber = true

-- Configure tab length and convert all tabs to spaces
opt.tabstop = 4
opt.shiftwidth = 4
opt.expandtab = true

-- Enable wrapping through lines
opt.whichwrap:append {
    ["h"] = true,
    ["l"] = true,
    ["<"] = true,
    [">"] = true,
    ["["] = true,
    ["]"] = true,
}

-- Do not break lines visually
opt.wrap = false

-- Specify where new buffers should appear
opt.splitbelow = true
opt.splitright = true
