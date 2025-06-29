import React from "react";

export default function SidebarData({satelliteState}) {
    if (!satelliteState) return <div> Awaiting Satellite Info... </div>;
    // const {name, velocity, altitude, latitude, longitude, attitude} = satelliteState;
    const {name, position_geo} = satelliteState;
    return (
		<div>
			<h2 className="text-xl font-bold mb-4"> Satellite Info </h2>
			<p> Name: {name} </p>
			<p> Latitude: {position_geo[0].toFixed(2)}° </p>
			<p> Longitude: {position_geo[1].toFixed(2)}° </p>
			<p> Altitude: {position_geo[2].toFixed(2)} km </p>
			{/* <p> Velocity: {velocity.toFixed(2)} km/s</p> */}
			{/* <p> Attitude: [{attitude.map(a => a.toFixed(2)).join(", ")}] </p> */}
		</div>
    );
}
