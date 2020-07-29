import React, { Component } from 'react';
import axios from 'axios';
import './App.css';
import Sections from './components/Sections/Sections'
import AUX from  './components/AUX/Aux'


class App extends Component {
  state = {
    getUrl: 'https://acf9n1kt36.execute-api.us-east-1.amazonaws.com/sandbox/get-service-names',
    postUrl: 'https://acf9n1kt36.execute-api.us-east-1.amazonaws.com/sandbox/get-sq-names',
    serviceNames: []

  }

  componentDidMount() {
  //use lifecyle method component did mount when invoking initial http request automatically 
   axios.get(this.state.getUrl).then(res => {
    let data = res.data
    data = data.replace("[","")
    data = data.replace("]","")
    const service_names = data.split(',')    
    this.setState({
      serviceNames: service_names
    })    
   })
  }

  render() {
    //transform serviceNames array into Sections objects - return JSX
     let transformed = this.state.serviceNames.map(serviceName => {
      return <Sections sname={serviceName} postUrl={this.state.postUrl}/>
    })    
    return (
      <AUX>
        {transformed}       
      </AUX>
    );
  }  
}

export default App;


//AWS Python React Boto3 Lambda API-Gateway Practice
//Obtain service quota information via http request using Boto3, Lambda and APIGW
//Show results in browser
//Elliott Arnold DMS DFW 7-28-20  Part 1  -> TBC 
//Covid19