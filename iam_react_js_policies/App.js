import React, {Component} from 'react';
import '/***/***/iam_viewer_modal_sidebar/iam-viewer/src/App.css'
import Sidebar from './component/SideBar/SideBar'
import Modal from './component/Modal/Modal'
import Aux from './Aux/Aux'

class App extends Component  {

  state = {
    policyArn: 
    ["arn:aws:iam::aws:policy/AdministratorAccess",
    "arn:aws:iam::aws:policy/AmazonCodeGuruProfilerFullAccess",
    "arn:aws:iam::aws:policy/AmazonDetectiveFullAccess"],
    url: "https://p3a7rd5ztb.execute-api.us-east-1.amazonaws.com/sandbox/iam-policy"
  }

 sideBarHandler = (event) => {
  let element = document.querySelector('#aside')
    console.log(event.target)       
    element.remove()
    
  
}
  render () {
    let element = this.state.policyArn.map((_,index) => {
      return  <Sidebar closesidebar={this.sideBarHandler} gatewayUrl={this.state.url}
      policyArn={this.state.policyArn[index]}/>
    })

  return ( 
    <Aux>
      <div id="main">         
        <Modal close={this.sideBarHandler}/>
         {element}           
      </div>     
    </Aux>
         
   )     
  }
  
}

export default App;

//AWS IAM ApiGateway Lambda Python React Compnents 
// Make request to ApiGateway return IAM policy document to browser
// Practice with Modals and Sidebars
// Elliott Arnold 7-19-20  
// Learning React JS - Need to learn CSS for real
