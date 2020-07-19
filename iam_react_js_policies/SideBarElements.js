import React, {Component} from 'react';
import Axios from 'axios'
import Aux from '../../Aux/Aux'
import '/***/***/iam_viewer_modal_sidebar/iam-viewer/src/App.css'
import Modal from  '/Users/ellarnol/iam_viewer_modal_sidebar/iam-viewer/src/component/Modal/Modal.js'


class SidebarElements extends Component  {

    state = {       
        url: "https://p3a7rd5ztb.execute-api.us-east-1.amazonaws.com/sandbox/iam-policy",
        policy: null 
        
      }      

    ajaxRequest = (url,policyArn) => {
        const params = {arn: policyArn, version:"v1"}    
        return Axios.post(url, params)      
    
    }
    // Handle click event -> pass arn to axios -> api gateway -> display in modal 
    apiGatewayHandler = (event,url) => {
      const  iamPolicy = event.target

      console.log(event.target)   
       this.ajaxRequest(url,iamPolicy.innerText).then(data => {
           const policy = data.data                        
           // policy must be stringified to display in browser 
           this.setState({
             policy: JSON.stringify(policy, null, 4)
           })                 
           
       }).catch(err => {
           console.log(err,'WTF')
       })
   
   }

      render ()  { 
        return (
            <Aux>
              
              <div >
                <ul >
                   <li >                   
                    <button  id="target" className="marked" 
                     onClick={(event) => this.apiGatewayHandler(event,this.props.gatewayUrl)}>
                      {this.props.arn}</button>                       
                    <button onClick={(event) => this.props.handler(event)}>Delete Policy</button>                                      
                    </li>     
                  </ul> 
              </div>           
 
              <div>                
                <Modal policyDoc={this.state.policy}/ >   

              </div>
            </Aux>
        )        

      }
    };



export default SidebarElements;

//AWS IAM ApiGateway Lambda Python React Compnents 
// Make request to ApiGateway return IAM policy document to browser
// Practice with Modals and Sidebars
// Elliott Arnold 7-19-20  
// Learning React JS - Need to learn CSS for real
