export async function getState() {
    const res = await fetch("http://localhost:8000/state")
    return res.json();
}
