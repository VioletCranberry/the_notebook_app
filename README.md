### The notebook app

Everything starts with the notebook app itself. This app allows
our users to insert JavaScript code, evaluate it and retrieve the
output.

### The solution

```text
Key Features:

- Incorporate multiple JavaScript code blocks
- Execute JavaScript code securely
- Dynamically remove code blocks while maintaining at least one

Security Measures:

- Default strict-mode prevents code from accessing filesystem or network
- Default execution time limit set to 10 seconds
- Default memory limit for code execution is 10Mb

```

### Why not a simple `eval` in the Browser (client-side)?

Using `eval` in the browser is dangerous because it can execute arbitrary code,
leading to security vulnerabilities like code injection attacks. Malicious code
can access and manipulate the DOM, steal data, or perform unauthorized actions.
For more details, refer to [MDN Web Docs on eval()](https://developer.mozilla.org/en-US/docs/Web/JavaScript/Reference/Global_Objects/eval).

### Why `window.Document` May Not Return Something?

`window.Document` refers to the `Document` object representing the webpage.
In a sandboxed environment like PyMiniRacer, there is no DOM to interact with,
hence `window.Document` will not behave as it does in a browser. This ensures a
secure and isolated execution context for JavaScript code.

### Why not PyV8 / STPyV8 V8 engine wrappers or PythonMonkey?

[PyV8](https://code.google.com/archive/p/pyv8/) and its fork [STPyV8](https://github.com/cloudflare/stpyv8),
which allow interoperability between Python 3 and JavaScript running on the Google V8 engine,
are not thread-safe. Using them with WSGI servers can often lead to segmentation faults.
Installing [PythonMonkey](https://github.com/Distributive-Network/PythonMonkey) on my Mac was pretty
problematic.

### Dependencies:

- Flask: [Flask Documentation](https://flask.palletsprojects.com/)
- PyMiniRacer: [PyMiniRacer repository](https://github.com/bpcreech/PyMiniRacer)

### Troubleshooting:

`RuntimeError: Native library not available` error:

```text

# 1. Find your site-packages
python -m site

# 2. Download the Dylib file
wget https://github.com/sqreen/PyMiniRacer/files/7575004/libmini_racer.dylib.zip

# 3. Unzip The Dylib file
unzip libmini_racer.dylib.zip

# 4. Move Dylib file to your site-packages
mv libmini_racer.dylib <site-packages-path/py_mini_racer/.>

```

### Docker testing

```bash

docker build -t the_notebook_app .
docker run --env-file .env -p 5000:5000 the_notebook_app
curl -X POST http://localhost:5000/run -H "Content-Type: application/json" -d \
  '{"script": "function test() { return \"Hello, world!\"; } test();"}'

{
  "result": "Hello, world!"
}

```

### Minikube testing

```bash

minikube start
eval $(minikube docker-env)
docker build -t the_notebook_app .
kustomize build manifests/overlays/minikube | kubectl apply -f -
kubectl port-forward --namespace the-notebook-app service/the-notebook-app 5000:5000
curl -X POST http://localhost:5000/run -H "Content-Type: application/json" -d \
  '{"script": "function test() { return \"Hello, world!\"; } test();"}'

{
  "result": "Hello, world!"
}

```
