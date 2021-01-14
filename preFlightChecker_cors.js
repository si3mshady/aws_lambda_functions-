const  exec = require('child_process').exec;
const express = require('express')
const bodyParser = require('body-parser')
const app = express();

app.set('view engine', 'ejs')
app.use(express.static("public"))
app.use(bodyParser.urlencoded({
    extended: true
}));

app.get('/', (req,res) => {  
    res.render('index')
})

app.post('/allowMethods', (req, res) => {    
    const url = req.body.endpoint
    exec(`curl -IX OPTIONS ${url} | grep -i access-control-allow-methods`,
    (err,stdout,_) => {
   if (!err) {
        const allowMethods = stdout.split(':')[1].split(',')   
       res.render('allowMethods', {"allowMethods": allowMethods})
    }
    })})

app.post('/allowHeaders', (req, res) => {    
        const url = req.body.endpoint    
        exec(`curl -IX OPTIONS  ${url}  | grep -i access-control-allow-headers`,
        (err,stdout,_) => {
       if (!err) {    
            const allowHeaders = stdout.split(':')[1].split(',')              
           res.render('allowHeaders', {"allowHeaders": allowHeaders})
        }
     })})

app.post('/allowOrigin', (req, res) => {    
        const url = req.body.endpoint    
        exec(`curl -IX OPTIONS  ${url}  | grep -i access-control-allow-origin`,
        (err,stdout,_) => {
       if (!err) {    
            const allowOrigin = stdout.split(':')[1].split(',')              
           res.render('allowOrigin', {"allowOrigin": allowOrigin})
        }
     })})
    
    

app.listen(3001, () => {
    console.log("Server started on port 3001")
})

// NodeJS API Gateway EJS Troubleshooting CORS with CURL font-end exercise  "Pre-flight checker"
// Create a small front end that leverages CURL utiltiy to check api attributes
// of an API for troubleshooting
//Elliott Arnold DMS 1-13-21  
