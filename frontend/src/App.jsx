import React, {useEffect, useState} from "react";
import Viewer3D from "./Viewer3D.jsx";
import SidebarData from "./SidebarData.jsx";
import {getState} from "./services/api.js";

export default function App() {
	const [state, setState] = useState(null);
	const [rotAngle, setRotAngle] = useState(0);
	const [speed, setSpeed] = useState(1.0);
	const [userLocation, setUserLocation] = useState(null);
	useEffect(() => {
		const fetchUserLocation = async () => {
			try {
				const res = await fetch('http://ip-api.com/json/');
				const data = await res.json();
				if (data.status === 'success') {
				const {lat, lon} = data;
					const res = await fetch(`http://10.147.17.201:8000/observer-eci?lat=${lat}&lon=${lon}`);
					const data2 = await res.json();
					setUserLocation(data2);
				}
			} catch (error) {
				console.error('Failed to fetch IP location:', error);
			}
		};
		fetchUserLocation();
	}, []);
	useEffect(() => {
		const fetchData = async () => {
			const data = await getState();
			setState(data);
    	};
		fetchData();
		if (speed == 0) return;
		const interval = setInterval(fetchData, 1000 / Math.abs(speed));
		return () => clearInterval(interval);
	}, [speed]);
	useEffect(() => {
		const fetchRotationAngle = async () => {
			const res = await fetch("http://10.147.17.201:8000/rotangle")
			const data = await res.json()
			setRotAngle(data);
    	};
		fetchRotationAngle();
	}, []);

	return (
		<div className="bg-gray-950 h-screen w-screen flex flex-row">
			<div className="flex-1 text-white p-5">
				<SidebarData speed={speed} setSpeed={setSpeed} state={state} />
			</div>
			<div className="flex-7">
				<Viewer3D rotationAngle={rotAngle} userLocation={userLocation} speed={speed} state={state} />
			</div>
		</div>
	);
}
