import React from 'react';

import '/***/***/iam_viewer_modal_sidebar/iam-viewer/src/App.css'

const modal = (props) => (
    
    <div >
    <div id="code" className="open-modal" >    

      <code> 
        <pre>
           <em> 
             {props.policyDoc} 
           </em> 
        </pre> 
      </code>     
    </div>
  </div>
     
);

export default modal


//https://stackoverflow.com/questions/130404/javascript-data-formatting-pretty-printer