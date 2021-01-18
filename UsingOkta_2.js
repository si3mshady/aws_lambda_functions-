const express = require('express')
const bodyParser = require('body-parser')
const app = express();

app.use(bodyParser.urlencoded({
    extended: true
}));


app.get('/', (req,res) => {  
   res.send('<h1>Authcode and JWT fetcher</h1>')
}) 


app.get('/authorization-code/callback', (req,res) => {  
    const authCode = res.req.query.code
    console.log(authCode)
    const data = { authcode: authCode  }
    res.setHeader('Content-Type','application/json')   
    res.json(data)
   
})

app.listen(8080, () => {
    console.log("Server started on port 8080")
})

//to serve callback http request needed for Oauth2 Authentication
//1-17-21 Elliott Arnold AWS DMS 
