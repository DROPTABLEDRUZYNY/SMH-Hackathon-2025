import TileData from "./tile-health";
import imieninyData from "@/public/zdrowie/imieniny.json";
import kartkaZKalendarzaData from "@/public/zdrowie/kartka_z_kalendarza.json";

//const CITY = 'Krakow';
//const API_KEY = process.env.REACT_APP_WEATHER_API_KEY;
//const URL = `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric&lang=pl`;

export  default async function TilesHealth() {
  const randomIndex = Math.floor(Math.random() * kartkaZKalendarzaData.length);
  const tilesData = kartkaZKalendarzaData[randomIndex];

  const weather = "Zachmurzenie duże, temperatura 12°C, wiatr 4 km/h"; // TODO: fetch from API
  //TODO PM10: 53

  const today = new Date();
  const dateForSearch = 
    `${String(today.getDate()).padStart(2, "0")}.${String(today.getMonth() + 1).padStart(2, "0")}`;
  const formattedDate = `${dateForSearch}.${today.getFullYear()}`;
  let todayNameDay = imieninyData.find((item) => item.date === dateForSearch);
  
  const daysOfWeek = [
    "Niedziela",
    "Poniedziałek",
    "Wtorek",
    "Środa",
    "Czwartek",
    "Piątek",
    "Sobota",
  ];
  const dayOfWeek = daysOfWeek[today.getDay()];

  if (!todayNameDay)
    todayNameDay = {
      date: "29.03",
      name_day: "Celina, Walerian",
    };


  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 ">
      <TileData
        tileData={{
          title: `${dayOfWeek} ${formattedDate}`,
          text: `Imieniny obchodzą dzisiaj: ${todayNameDay.name_day}`,
        }}
      />
      <TileData tileData={{ title: "Pogoda", text: weather }} />
      <TileData
        tileData={{ title: "EKO Porada", text: tilesData.health_advise }}
      />
      <TileData
        tileData={{
          title: "Jak oszczędzać?",
          text: tilesData.healthy_meal,
        }}
      />
      <TileData tileData={{ title: "PM 10:", text: "53", variant:3  }} />
      <TileData tileData={{ title: "PM 2,5:", text: "81", variant:1 }} />
    </div>
  );
}

