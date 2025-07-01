import {useRef, useEffect} from "react";
import {Canvas, useFrame} from "@react-three/fiber";
import {OrbitControls, Stars} from "@react-three/drei";
import {useLoader} from '@react-three/fiber';
import {TextureLoader, EdgesGeometry, LineSegments, LineBasicMaterial, Vector3, ArrowHelper} from 'three';
const earthTexture = '/assets/earth.jpg';

const SUN_RADIUS = 695508 
const EARTH_RADIUS = 6371
const EARTH_BASE_RADIUS = 50
const SATELLITE_SIDE = 100
const SCALE = 10 / EARTH_RADIUS
const ARROW_SCALE = 0.5;
const ROTATION_ANGLE = 0;

function Sun({position}) {
	if (position == null) return;
	const positionX = SCALE * position[1];
	const positionY = SCALE * position[2];
	const positionZ = SCALE * position[0];
	return (
		<>
			<mesh position={[positionX, positionY, positionZ]}>
				<sphereGeometry args={[SUN_RADIUS * SCALE, 64, 64]} />
				<meshStandardMaterial color="yellow" emissive="yellow" emissiveIntensity={10} toneMapped={false} />
			</mesh>
			<directionalLight position={[positionX, positionY, positionZ]} intensity={1.5} color="white" castShadow />
		</>
	);
}

function Earth({simulationSpeed, observerPosition, angle}) {
	const earthRef = useRef();
	useFrame((_, delta) => {
		if (earthRef.current) {
			const rotationSpeed = (2 * Math.PI) / 86164; // radians/sec
			earthRef.current.rotation.y += delta * rotationSpeed * simulationSpeed;
		}
	});
	if (observerPosition == null) return;
	const positionX = SCALE * observerPosition[1];
	const positionY = SCALE * observerPosition[2];
	const positionZ = SCALE * observerPosition[0];
	const texture = useLoader(TextureLoader, earthTexture);
	return (
		<group ref={earthRef}>
			<mesh rotation={[0, angle, 0]}>
				<sphereGeometry args={[EARTH_RADIUS * SCALE, 64, 64]} />
				<meshStandardMaterial map={texture} />
			</mesh>
			<mesh position={[positionX, positionY, positionZ]}>
				<sphereGeometry args={[EARTH_BASE_RADIUS * SCALE, 64, 64]} />
				<meshStandardMaterial color="red" />
			</mesh>
		</group>
	);
}

function Satellite({position, velocity, sun}) {
	if (position == null) return;
	const meshRef = useRef();
	useEffect(() => {
		if (!meshRef.current) return;
		const geometry = meshRef.current.geometry;
		const edges = new EdgesGeometry(geometry); 
		const lines = new LineSegments(edges, new LineBasicMaterial({color: "black"}));
		meshRef.current.add(lines);
	},)
	const positionX = SCALE * position[1]; const positionY = SCALE * position[2]; const positionZ = SCALE * position[0];
	const velocityX = SCALE * velocity[1]; const velocityY = SCALE * velocity[2]; const velocityZ = SCALE * velocity[0];
	const sunX = SCALE * sun[1]; const sunY = SCALE * sun[2]; const sunZ = SCALE * sun[0];

	const earthDir = new Vector3(positionX, positionY, positionZ).multiplyScalar(-1).normalize();
	const velocityDir = new Vector3(velocityX, velocityY, velocityZ).normalize();
	const sunDir = new Vector3(sunX, sunY, sunZ).normalize();
	return (
		<group position={[positionX, positionY, positionZ]}>
			<mesh ref={meshRef}>
				<boxGeometry args={[SATELLITE_SIDE * SCALE, SATELLITE_SIDE * SCALE, SATELLITE_SIDE * SCALE]}/>
				<meshStandardMaterial color="red"/>
			</mesh>
			<primitive object={new ArrowHelper(earthDir, new Vector3(0, 0, 0), ARROW_SCALE, 0x00ffff)}/>
			<primitive object={new ArrowHelper(velocityDir, new Vector3(0, 0, 0), ARROW_SCALE, 0xff00ff)}/>
			<primitive object={new ArrowHelper(sunDir, new Vector3(0, 0, 0), ARROW_SCALE, 0xffff00)}/>
		</group>
	);
}

export default function Viewer3D({rotationAngle, userLocation, state, speed}) {
    return (
		<div className="w-full h-full">
			<Canvas camera={{position: [0, 0, 20]}}>
				<ambientLight intensity={0.15}/>
				<Stars/>
				<Sun position={state ? state.sun_eci : null} />
				<Earth simulationSpeed={speed} observerPosition={userLocation ? userLocation : null} angle={rotationAngle}/>
				<Satellite position={state ? state.position_eci : null} velocity={state ? state.velocity_eci : null} sun={state ? state.sun_eci : null}/>
				<OrbitControls enableZoom={false} target={[0, 0, 0]}/>
			</Canvas>
		</div>
    );
}
  