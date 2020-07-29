import React from 'react';
import AUX from '../AUX/Aux'
import Articles from '../Articles/Articles'

const section = (props) => (
  // passing props App.js -> Sections.js -> Articles.js 
    <AUX>
         <section >           
             <Articles sname={props.sname} postUrl={props.postUrl} />
         </section>
    </AUX>
 
)

export default section;


//AWS Python React Boto3 Lambda API-Gateway Practice
//Obtain service quota information via http request using Boto3, Lambda and APIGW
//Show results in browser
//Elliott Arnold DMS DFW 7-28-20  Part 1  -> TBC 
//Covid19