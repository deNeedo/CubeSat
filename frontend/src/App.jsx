import React, {useEffect, useState} from "react";
import Viewer3D from "./Viewer3D";
import SidebarData from "./SidebarData";
import {getSatelliteState} from "./services/api";

export default function App() {
	const [satelliteState, setSatelliteState] = useState(null);

	useEffect(() => {
		const fetchData = async () => {
			const data = await getSatelliteState();
			setSatelliteState(data);
    	};
		fetchData();
		const interval = setInterval(fetchData, 1000);
		return () => clearInterval(interval);
	}, []);

	return (
		<div className="bg-gray-950 h-screen w-screen flex flex-col">
			<div className="flex-1">
				<Viewer3D satelliteState={satelliteState} />
			</div>
			<div className="h-1/5 text-white p-4 overflow-y-auto">
				<SidebarData satelliteState={satelliteState} />
			</div>
		</div>
	);
}
