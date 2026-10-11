# Neovim

## Questions

- [ ] Removing & Creating files
- [ ] Surround with         ++  
- [ ] Buffers               ++
- [ ] Buffers and clipboard ++
- [ ] Features i am missing? 
- [ ] Better interactgion with Tabs and copilot

## Vim Keybindings and Commands

  - <Tab > - Accept Copilot suggestion (only when no completion menu is open)
  - Ctrl+n/Ctrl+p - Next/previous Copilot suggestions
  - <Ctrl >+e - Dismiss suggestion


  Main Commands:
  - <leader>cp - Toggle Copilot Chat (most important)
  - <leader>cpo - Open chat window
  - <leader>cc - Close chat window


  Claude Code Integration:
  - <leader>ai - Toggle Claude Code window
  - <leader>an - Start new Claude conversation

  Normal Mode:

  - ys<motion><char> - Add surroundings (e.g., ysiw" adds quotes around word)
  - yss<char> - Add surroundings around entire line
  - yS<motion><char> - Add surroundings on new lines
  - ySS<char> - Add surroundings around entire line on new lines
  - ds<char> - Delete surroundings (e.g., ds" removes quotes)
  - cs<old><new> - Change surroundings (e.g., cs"' changes quotes to single quotes)
  - cS<old><new> - Change surroundings on new lines

  Visual Mode:

  - S<char> - Add surroundings around selection
  - gS<char> - Add surroundings around selection on new lines

  Insert Mode:

  - <C-g>s<char> - Add surroundings
  - <C-g>S<char> - Add surroundings on new lines

## NvimTree

`:NvimTreeToggle` - Open NvimTree
`:NvimTreeFindFile` - Find file in NvimTree

`a` - Create file 
    `/` - Create folder
`d` - Delate file
`m` - Marking file

## Screen manimpulations

- `:vsplit` -vertical split
- `:split` - horizontal split
`:NvimTreeToggle` - Open NvimTree
`:NvimTreeFindFile` - Find file in NvimTree

## Quick notes 

- **Hide Tabline** 
    - `set showtabline=0`
- **Hide Line Numbers**
    - `set nonu`
- **Hide Status Line**
    - `set laststatus=0`
- `<C>` + `w` + `v` - Split window vertically
- **Open a file in a new tab**
    - `:tabnew filename`
- **Create new file incide neovim**
    - `:e filename`branch
