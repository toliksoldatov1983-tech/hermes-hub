import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path = "./output/Юля_фасады_выборка_90_Малярка.xlsx";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path));

for (const name of ["6010-R90B", "1000-N"]) {
  const s = wb.worksheets.getItem(name);
  s.mergeCells("D2:H2");
  s.getRange("D2").values = [["ВЕСЬ ЗАКАЗ"]];
  s.getRange("D2:H2").format = {
    fill: "#1F4E78",
    font: { bold: true, color: "#FFFFFF", size: 12 },
    horizontalAlignment: "center",
  };
  for (const row of [3,4,5,6,7]) s.mergeCells(`D${row}:G${row}`);
  s.getRange("D3:D7").values = [["Общее количество деталей"],["Общая квадратура, м²"],["Фрезерованная выборка, м²"],["Модерн, м²"],["Витрина, м²"]];
  s.getRange("H3:H7").formulas = [["='Общий итог'!C6"],["='Общий итог'!D6"],["='Общий итог'!D10"],["='Общий итог'!D11"],["='Общий итог'!D12"]];
  s.getRange("D3:H7").format = {
    fill: "#EAF2F8",
    borders: { preset: "all", style: "thin", color: "#8EA9C1" },
  };
  s.getRange("D3:D7").format.font = { bold: true };
  s.getRange("H3:H7").format = { fill: "#D9EAD3", font: { bold: true }, horizontalAlignment: "right", borders: { preset: "all", style: "thin", color: "#93C47D" } };
  s.getRange("H3").format.numberFormat = "0";
  s.getRange("H4:H7").format.numberFormat = "0.000000";
}

const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(path);
for (const [name, file, range] of [["6010-R90B","visible6010.png","A1:J14"],["1000-N","visible1000.png","A1:J14"],["Общий итог","visible_summary.png","A1:D13"]]) {
  const blob = await wb.render({sheetName:name,range,scale:1.3,format:"png"});
  await fs.writeFile(`./output/${file}`,new Uint8Array(await blob.arrayBuffer()));
}
console.log((await wb.inspect({kind:"table",range:"6010-R90B!A1:J14",include:"values,formulas",tableMaxRows:14,tableMaxCols:10})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"})).ndjson);
