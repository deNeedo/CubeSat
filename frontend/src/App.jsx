import React, {useEffect, useState} from "react";
import Viewer3D from "./Viewer3D";
import SidebarData from "./SidebarData";
import {getState} from "./services/api";

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
					const res = await fetch(`http://localhost:8000/observer-eci?lat=${lat}&lon=${lon}`);
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
		const interval = setInterval(fetchData, 500 / speed);
		return () => clearInterval(interval);
	}, [speed]);
	useEffect(() => {
		const fetchRotationAngle = async () => {
			const res = await fetch("http://localhost:8000/rotangle")
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
			<div className="flex-9">
				<Viewer3D rotationAngle={rotAngle} userLocation={userLocation} speed={speed} state={state} />
			</div>
		</div>
	);
}
