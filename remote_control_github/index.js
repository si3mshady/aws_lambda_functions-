
getAllButtons = () => {
    var  buttons = $(".keypad-btn")
    return  Array.from(buttons)   
}

// create api that sends instance-id's 
setDataAttributes = (instance_list) => {   
    buttons = getAllButtons()
    buttons.forEach((element, index) => { $(element).attr("data-instance",instance_list[index])});
}

setClickListeners = () => {
    buttons = getAllButtons()
    buttons.forEach(element => { $(element).click( () => {
        // get data property of each element w/ jquery 
        var instance_id = $(element).data().instance
        console.log(instance_id)        
        // display data property of each button in input div
        $("#input").text(() => {
            return instance_id })})})}

get_ec2_instances = () => {
    const url = "https://ra8npboyu6.execute-api.us-east-1.amazonaws.com/api/"
    axios.get(url)
    .then(res => {      
        var instances = JSON.parse(res.data.body)        
        setDataAttributes(instances)            
    }).catch( err => {console.log(err)})}

setToggleButton = () => {
    $('#toggle').click( () => {
        // get content of input space -> when button is pressed simulate led red light, on/off visual 
        $(".led").css('background-color','red')
        setTimeout(() => { $(".led").css('background-color','white')}, 100);
        var instance_id = $("#input").text()               
        console.log(instance_id)
        const toggleUrl = `https://ra8npboyu6.execute-api.us-east-1.amazonaws.com/api/${instance_id}`       
        axios.get(toggleUrl) .then(res => { console.log(res) }).catch(err => { console.log(err) })})}

setToggleButton()
setClickListeners()
get_ec2_instances()

//AWS Chalice ApiGateway Lambda Python JS Jquery CSS practice
//Create a small remote control to turn on/off ec2 instances - use bootstrap and css
//Elliott Arnold 
//10-4-20 Covid 19 
