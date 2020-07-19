import React from 'react';
import '/***/***/iam_viewer_modal_sidebar/iam-viewer/src/App.css'
import SBE from './SideBarElements'
import Aux from '/Users/ellarnol/iam_viewer_modal_sidebar/iam-viewer/src/Aux/Aux.js'


const sidebar = (props) => (    
    <Aux>
    <div id="aside">
    <aside > 
            <div >
                  <SBE closesidebar={props.closesidebar}
                   handler={props.closesidebar}
                   arn={props.policyArn} 
                   gatewayUrl={props.gatewayUrl} />    
            </div>              
 
    </aside> 
        </div>
    </Aux>     
);

export default sidebar

//AWS IAM ApiGateway Lambda Python React Compnents 
// Make request to ApiGateway return IAM policy document to browser
// Practice with Modals and Sidebars
// Elliott Arnold 7-19-20  
// Learning React JS - Need to learn CSS for real
