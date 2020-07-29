import React, { Component } from 'react';
import axios from 'axios'
import Aux from '../AUX/Aux'
import '/...App.css';

class Articles extends Component {
    //always use class components and state when preforming async tasks and 
    // when one needs to re-render DOM elements 
    state = {
        service_names: ''
    }

    toggleView = (event) =>  {   
        //the 'p' tag is adjacent to the button which is using the 'hide' class     
        const paragraph = event.target.nextSibling
        paragraph.classList.toggle('hide')
    }
    
    getServiceName = (event,postUrl) => {    
         //the 'p' tag is adjacent to the button, retrieving the innerText and using it for post request 
        const service_name = event.target.nextSibling.innerText
        const param  = {"service": service_name}
        axios.post(postUrl,param).then(data => {            
            const serviceQuotaNames = new String(data.data);
            console.log(serviceQuotaNames)
            this.setState({ service_names: serviceQuotaNames  })           
        })
    }

    render () {
        return (

    <Aux>
     <div>
        <article>
        <div>
        <button onClick={(event) => this.getServiceName(event,this.props.postUrl)}
        type="button"> Get Service Quota Names </button>

         <p> {this.props.sname} </p>
         <button onClick={(event) => this.toggleView(event)} 
               className='toggle' type="button"> +/- </button>
         <p className='hide'> {this.state.service_names} </p>
        </div>         
        </article>
     </div>  
   </Aux>
        )
    }
}

export default Articles;


//AWS Python React Boto3 Lambda API-Gateway Practice
//Obtain service quota information via http request using Boto3, Lambda and APIGW
//Show results in browser
//Elliott Arnold DMS DFW 7-28-20  Part 1  -> TBC 
//Covid19