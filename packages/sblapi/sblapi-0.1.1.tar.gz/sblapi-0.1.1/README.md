# Shield Bot List API
Hey, welcome to the Shield Bot List API. Lets get straight to the point!

## Authors

- [The Team](https://www.github.com/Shield-Bot-List)

  

  


  
## Support

For support, you may create a private ticket or go in the help channel in our discord.

Discord: https://discord.gg/rmZkZPR5CX

## Usage/Examples

### Server Count Post


```python
import sblapi

response = sblapi.sblapi('botid', 'authtoken', guildcount)
print(response.text)

```
### Get Likes Last 24 hours

```python

import sblapi

response = sblapi.getlikes('botid', 'authtoken')
print(response.text)

```

# Thank you for using *Shield Bot List*