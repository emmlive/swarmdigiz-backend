(function(){

const API = "https://app.swarmdigiz.com/api/inspection";

function createWidget(){

const widget = document.createElement("div");
widget.id = "swarmdigiz-widget";

widget.innerHTML = `
<div style="
position:fixed;
bottom:20px;
right:20px;
width:320px;
background:white;
border-radius:12px;
box-shadow:0 10px 30px rgba(0,0,0,.2);
font-family:sans-serif;
padding:20px;
z-index:9999">

<h3>Quick Air Duct Inspection</h3>

<select id="service">
<option value="air_duct">Air Duct Cleaning</option>
<option value="dryer_vent">Dryer Vent Cleaning</option>
<option value="carpet">Carpet Cleaning</option>
</select>

<br><br>

<input id="home_size" placeholder="Home size sq ft"/>

<br><br>

<button id="runInspection">
Run Inspection
</button>

<div id="quoteResult"></div>

</div>
`;

document.body.appendChild(widget);

document.getElementById("runInspection").onclick = runInspection;

}

async function runInspection(){

const service = document.getElementById("service").value;
const size = document.getElementById("home_size").value;

const payload = {
service_type: service,
home_size: size,
business_id: 1
};

const res = await fetch(API,{
method:"POST",
headers:{'Content-Type':'application/json'},
body:JSON.stringify(payload)
});

const data = await res.json();

document.getElementById("quoteResult").innerHTML =
`Estimated Quote: $${data.quote}`;

}

createWidget();

})();