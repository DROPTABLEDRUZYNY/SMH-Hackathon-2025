import TileData from "./tile-data";
import ecoTipsData from "@/public/be-eco/eco-tips.json";
import moneyTipsData from "@/public/be-eco/money-tips.json";

//const CITY = 'Krakow';
//const API_KEY = process.env.REACT_APP_WEATHER_API_KEY;
//const URL = `https://api.openweathermap.org/data/2.5/weather?q=${CITY}&appid=${API_KEY}&units=metric&lang=pl`;

export  default async function TilesData() {
  const ecoTip = ecoTipsData['eco_tips'][Math.floor(Math.random() * ecoTipsData['eco_tips'].length)];
  const moneyTip = moneyTipsData['money_tips'][Math.floor(Math.random() * moneyTipsData['money_tips'].length)];

  // const weather = "Zachmurzenie duże, temperatura 12°C, wiatr 4 km/h"; // TODO: fetch from API
  // const today = new Date();
  // const dateForSearch = 
  //   `${String(today.getDate()).padStart(2, "0")}.${String(today.getMonth() + 1).padStart(2, "0")}`;
  // const formattedDate = `${dateForSearch}.${today.getFullYear()}`;

  return (
    <div className="grid grid-cols-1 gap-4 lg:grid-cols-2 ">
      {/* <TileData
        tileData={{
          title: `${dayOfWeek} ${formattedDate}`,
          text: `Imieniny obchodzą dzisiaj: ${todayNameDay.name_day}`,
        }}
      />
      <TileData tileData={{ title: "Pogoda", text: weather }} /> */}

      <TileData tileData={{ title: "PM 10:", text: "53", variant: 2  }} />
      <TileData tileData={{ title: "PM 2,5:", text: "81", variant: 1 }} />

      <TileData
        tileData={{ title: "EKO Porada", text: ecoTip }}
      />
      <TileData
        tileData={{
          title: "Jak oszczędzać?",
          text: moneyTip,
        }}
      />

    </div>
  );
}

