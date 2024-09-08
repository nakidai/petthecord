PetTheCord
--
This is a Web API for petting any user you know which has avatar

## Setup
Create some discord application (it is needed for getting discord user's avatar)
and put its token to `PETTHECORD_TOKEN` env var or write it to file and create
`PETTHECORD_TOKEN_FILE` env var with the path of the file with the token. Other
help is desribed in the `--help`.

## Usage
`https://example.com/<UserID>.gif` will return you gif that specified user.

To get UserID you should enable developer mode in your client and "Copy User ID"
option will appear when you do RMB on user.

### Instances
Also there's a working instance of this thing which is located at
`ptc.nakidai.ru`
