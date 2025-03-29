interface TileData {
  title: string;
  text: string;
  variant?: 1 | 2 | 3;
}

export default function TileData({ tileData }: { tileData: TileData }) {
  const gradientClasses = {
    1: "bg-gradient-to-br from-red-500/20 via-red-400/10 to-red-500/20",
    2: "bg-gradient-to-br from-yellow-500/20 via-yellow-400/10 to-yellow-500/20",
    3: "bg-gradient-to-br from-green-500/20 via-green-400/10 to-green-500/20",
  };
  const variant_classes = tileData.variant ? gradientClasses[tileData.variant] : "bg-white/5";

  return (
    <div className="bg-white/5 backdrop-blur-lg rounded-2xl border border-white/10 hover:border-white/20 transition-all duration-300 overflow-hidden">
      <div className="flex flex-row items-center justify-between px-7 py-4 w-full">
        <div className="min-w-0 mr-2">
          <h2 className="text-2xl font-semibold text-white tracking-tight">{tileData.title}</h2>
        </div>
      </div>

      <div className={`flex flex-col w-full px-7 py-6 ${variant_classes}`}>
        <p className="text-xl text-gray-200 leading-relaxed">{tileData.text}</p>
      </div>
    </div>
  );
}
