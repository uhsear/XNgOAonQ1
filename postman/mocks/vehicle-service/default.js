const http = require("http");
const PORT = process.env.PORT || 4501;
const JSON_HEADER = { "Content-Type": "application/json" };

const server = http.createServer((req, res) => {
  const { method, url } = req;

  // @endpoint GET /vehicles
  if (method === "GET" && url === "/vehicles") {
    res.writeHead(200, JSON_HEADER);
    return res.end(JSON.stringify([
      {
        "id": 1,
        "nickName": "The Lisa Marie",
        "vin": "4M2DV11W4RDJ53329",
        "make": "Mercury",
        "model": "Villager",
        "year": "1994",
        "miles": 159864
      },
      {
        "id": 2,
        "nickName": "Dolly",
        "vin": "JN8AZ2KR1AT169594",
        "make": "Nissan",
        "model": "Cube",
        "year": "2010",
        "miles": 59000
      }
    ]));
  }

  // @endpoint POST /vehicles
  if (method === "POST" && url === "/vehicles") {
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      let parsed = {};
      try { parsed = body ? JSON.parse(body) : {}; } catch (e) {}
      res.writeHead(201, JSON_HEADER);
      res.end(JSON.stringify({
        "id": 1,
        "nickName": parsed.nickName || "The Lisa Marie",
        "vin": parsed.vin || "4M2DV11W4RDJ53329",
        "make": parsed.make || "Mercury",
        "model": parsed.model || "Villager",
        "year": parsed.year || "1994",
        "miles": parsed.miles || "159,864"
      }));
    });
    return;
  }

  // @endpoint GET /vehicles/:id
  const getVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (method === "GET" && getVehicleMatch) {
    const id = parseInt(getVehicleMatch[1], 10);
    if (id === 0) {
      res.writeHead(404, JSON_HEADER);
      return res.end(JSON.stringify({ "message": "Vehicle with id: 0 not found." }));
    }
    res.writeHead(200, JSON_HEADER);
    return res.end(JSON.stringify({
      "id": id,
      "nickName": "The Lisa Marie",
      "vin": "4M2DV11W4RDJ53329",
      "make": "Mercury",
      "model": "Villager",
      "year": "1994",
      "miles": 159864
    }));
  }

  // @endpoint PATCH /vehicles/:id
  const patchVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (method === "PATCH" && patchVehicleMatch) {
    const id = parseInt(patchVehicleMatch[1], 10);
    let body = "";
    req.on("data", (chunk) => (body += chunk));
    req.on("end", () => {
      let parsed = {};
      try { parsed = body ? JSON.parse(body) : {}; } catch (e) {}
      res.writeHead(200, JSON_HEADER);
      res.end(JSON.stringify({
        "id": id,
        "nickName": parsed.nickName || "The Lisa Marie",
        "vin": parsed.vin || "4M2DV11W4RDJ53329",
        "make": parsed.make || "Mercury",
        "model": parsed.model || "Villager",
        "year": parsed.year || "1994",
        "miles": parsed.miles || 159999
      }));
    });
    return;
  }

  // @endpoint DELETE /vehicles/:id
  const deleteVehicleMatch = url.match(/^\/vehicles\/(\d+)$/);
  if (method === "DELETE" && deleteVehicleMatch) {
    res.writeHead(204, JSON_HEADER);
    return res.end("");
  }

  res.writeHead(404, JSON_HEADER);
  res.end(JSON.stringify({
    "error": "Endpoint not defined",
    "message": `No mock route defined for ${method} ${url}`
  }));
});

server.listen(PORT, () => console.log("Vehicle Service Mock running on port " + PORT));
