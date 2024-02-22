# Refresing your filesystem with using Bash on your ZI VMs

## It's as easy as this

- First cipher your password and save to a file
- Then read & decipher it
- And use it in kinit command

Boom, you've refreshed your filesystem :)

### First create a key file, so every time you do not need to enter a key
- `openssl rand -base64 32 > ~/aes_key_file.key`

### Now cipher your ZI password
- `echo "YourPasswordHere" | openssl enc -aes-256-cbc -pbkdf2 -salt -pass file:/zi/home/user.name/aes_key_file.key -out /zi/home/user.name/encrypted_password.enc`
- Don't forget to change `user.name` and `YourPasswordHere` accordingly

## Now comes the crontab part
- First start a terminal and type this: `crontab -e`
- You'll most probably start the VIM. 
- Then, handle the crontab routines. I usually use this webpage to handle [it](https://crontab.guru/). It's rather easier to do with it.

### Set key location and encrypted pass locations
- Get your crontab routine, and change the `0 0 * * *` part accordingly from the line below:
- ``` 0 0 * * * encrypted_password_file="/zi/home/user.name/encrypted_password.enc" && key_file="/zi/home/user.name/aes_key_file.key" && kinitpwd=$(openssl enc -d -aes-256-cbc -pbkdf2 -salt -pass file:"$key_file" -in "$encrypted_password_file") && echo "$kinitpwd" | kinit```
- Now copy this into a text editor, change the `user.name` variables with your ZI username and finally copy and paste this to the VIM 
  - You can do this by first going to the terminal where the VIM is open.
  - Press `i` once to start editing mode
  - Go to the first uncommented line, i.e. line that does not start with a `#` 
  - Then paste with `ctrl+shift+V` to VIM.
- Finally quit the VIM with save by hitting `esc` button once and typing `:wq` and pressing `enter` once.
- Now your crontab should be set!

## Risks
- You might get locked out of your system if you enter 3 consecutive false passwords!
- IT kicking my ass because of this half-ass secure stuff :D
- Be careful and not forget to change the `user.name` and `YourPasswordHere` parts!
- **I have 0 responsibility in the case of you breaking your VM or your pass getting leaked! Use this at your own risk!!**

# Once again!
## I have 0 responsibility in the case of you breaking your VM or your pass getting leaked! Use this at your own risk!!