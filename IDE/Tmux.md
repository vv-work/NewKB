Certainly! Here's a concise markdown handbook on basic `tmux` commands:

---

# **TMUX Quick Handbook**

### **Session Management**

- **Start New Session:** `tmux`
- **Start Named Session:** `tmux new -s session_name`
- **Detach from Session:** `Ctrl + b, d`
- **List Sessions:** `tmux ls`
- **Attach to Session:** `tmux attach-session -t session_name`

### **Window Management**

- **Create Window:** `Ctrl + b, c`
- **Switch Window:** `Ctrl + b, <window number>`
- **Rename Window:** `Ctrl + b, ,`
- **List Windows:** `Ctrl + b, w`
- **Close Window:** `Ctrl + b, &`

### **Pane Management**

- **Split Horizontally:** `Ctrl + b, %`
- **Split Vertically:** `Ctrl + b, "`
- **Switch Pane:** `Ctrl + b, <arrow key>`
- **Toggle Pane Layout:** `Ctrl + b, space`
- **Resize Pane:** `Ctrl + b, <resize key>`

### **Miscellaneous**

- **Help:** `Ctrl + b, ?`
- **Reload Configuration:** `tmux source-file ~/.tmux.conf`

### **Other Useful Commands**

- **Execute Command in All Panes:** `Ctrl + b, :setw synchronize-panes`
- **Copy Mode:** `Ctrl + b, [`
  - **Navigation:** `↑, ↓, PgUp, PgDown`
  - **Copy:** `Ctrl + Space (start), Alt + w (copy), Ctrl + b, ] (paste)`

---

This should cover the essential commands and functionalities for using `tmux` effectively!
