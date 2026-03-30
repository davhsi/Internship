// async function getData() { // aync fn always returns a promise
//     return "hi"
// }

// const data = getData();
// console.log(data)

// data.then((res) => console.log(res)) 


const p1 = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("p1")
    }, 5000)
});

const p2 = new Promise((resolve, reject) => {
    setTimeout(() => {
        resolve("p2")
    }, 10000)
})

async function handlePromise() {
    console.log("helloooo world");
    const val1 =  await p1;
    console.log(val1);

    const val2 = await p2;
    console.log(val2);
}

handlePromise();