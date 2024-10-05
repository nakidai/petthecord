# FOR PEOPLE WHO JUST WANNA USE IT
Click [there](https://discord.com/oauth2/authorize?client_id=1280933495845290005) and use the `/petpet` command

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
`ptc.pwn3t.ru`

# Other petpet APIs
This project was rewritten several times, so this is a list of simillar APIs:

- [messengernew/petpet-api](https://github.com/messengernew/petpet-api)
 - Written in **Rust**
 - Instance: [`https://petpet.quadratik.pro/`](https://petpet.quadratik.pro/)

- [wavy-cat/petpet-go](https://github.com/wavy-cat/petpet-go)
 - Written in **Go**
 - Instance: [`https://pet.wavycat.ru/`](https://pet.wavycat.ru/)

- [nakidai/cptc](https://github.com/nakidai/cptc)
 - Written in **C**
 - There're no any instances of it :<
