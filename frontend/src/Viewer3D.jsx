import {useRef, useEffect} from "react";
import {Canvas} from "@react-three/fiber";
import {OrbitControls, Stars} from "@react-three/drei";
import {useLoader} from '@react-three/fiber';
import {TextureLoader, EdgesGeometry, LineSegments, LineBasicMaterial} from 'three';
import earthTexture from './assets/earth.jpg';

const SCALE = 8 / 6371 // size of Earth in three.js / Earth radius

function Earth() {
	const texture = useLoader(TextureLoader, earthTexture);
	return (
		<mesh position={[0, 0, 0]} rotation={[0, Math.PI/2, 0]}> // no idea why this rotation but it works (more less)
			<sphereGeometry args={[8, 64, 64]} />
			<meshStandardMaterial map={texture} />
		</mesh>
	);
}

function Satellite({position}) {
	if (position == null) return;
	const meshRef = useRef();
	useEffect(() => {
		if (!meshRef.current) return;
		const geometry = meshRef.current.geometry;
		const edges = new EdgesGeometry(geometry); 
		const lines = new LineSegments(edges, new LineBasicMaterial({color: "black"}));
		meshRef.current.add(lines);
	},)
	const positionX = SCALE * position[1];
	const positionY = SCALE * position[2];
	const positionZ = SCALE * position[0];
	return (
		<mesh ref={meshRef} position={[positionX, positionY, positionZ]}>
			<boxGeometry args={[0.3, 0.3, 0.3]}/>
			<meshStandardMaterial color="red"/>
	  	</mesh>
	);
}

export default function Viewer3D({satelliteState}) {
    return (
		<div className="w-full h-full">
			<Canvas camera={{position: [20, 0, 0]}}>
				<ambientLight intensity={2}/>
				<Stars/>
				<Earth/>
				<Satellite position={satelliteState ? satelliteState.position_eci : null}/>
				<OrbitControls enableZoom={false} target={[0, 0, 0]}/>
			</Canvas>
		</div>
    );
}
  