export async function getState() {
    const res = await fetch("http://10.147.17.201:8000/state")
    return res.json();
}
