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
import SBLApi

SBLApi.sblapi()

```
### Get Likes Last 24 hours

```javascript

const likeAPI = new APIs.likeApi('authtoken', client);
likeAPI.init().then(textRep => {
    const response = JSON.parse(textRep);
    console.log(response.users.length);
});
// parse it so you can access JSON props.

```

# Thank you for using *Shield Bot List*