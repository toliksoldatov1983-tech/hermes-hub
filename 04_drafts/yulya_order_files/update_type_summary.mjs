import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path = "./output/Юля_фасады_выборка_90_Малярка.xlsx";
const wb = await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s = wb.worksheets.getItem("Общий итог");

s.mergeCells("A8:D8");
s.getRange("A8").values = [["Итог по типу деталей"]];
s.getRange("A8:D8").format = {
  fill: "#1F4E78",
  font: { bold: true, color: "#FFFFFF", size: 13 },
  horizontalAlignment: "center",
};
s.getRange("A9:D13").values = [
  ["Тип", "Размерных строк", "Деталей", "Площадь, м²"],
  ["Фрезерованная выборка", null, null, null],
  ["Модерн", null, null, null],
  ["Витрина", null, null, null],
  ["Весь заказ", null, null, null],
];

const formulas = {
  10: "Выборка",
  11: "Модерн",
  12: "Витрина",
};
for (const [row, type] of Object.entries(formulas)) {
  s.getRange(`B${row}`).formulas = [[`=COUNTIF('6010-R90B'!B9:B30,\"${type}\")+COUNTIF('1000-N'!B9:B19,\"${type}\")`]];
  s.getRange(`C${row}`).formulas = [[`=SUMIF('6010-R90B'!B9:B30,\"${type}\",'6010-R90B'!F9:F30)+SUMIF('1000-N'!B9:B19,\"${type}\",'1000-N'!F9:F19)`]];
  s.getRange(`D${row}`).formulas = [[`=SUMIF('6010-R90B'!B9:B30,\"${type}\",'6010-R90B'!H9:H30)+SUMIF('1000-N'!B9:B19,\"${type}\",'1000-N'!H9:H19)`]];
}
s.getRange("B13:D13").formulas = [["=SUM(B10:B12)", "=SUM(C10:C12)", "=SUM(D10:D12)"]];
s.getRange("A9:D9").format = {
  fill: "#4472C4",
  font: { bold: true, color: "#FFFFFF" },
  horizontalAlignment: "center",
  borders: { preset: "all", style: "thin", color: "#D9E2F3" },
};
s.getRange("A10:D12").format = { borders: { preset: "all", style: "thin", color: "#D9D9D9" } };
s.getRange("A10:D10").format.fill = "#FFF2CC";
s.getRange("A11:D11").format.fill = "#DDEBF7";
s.getRange("A12:D12").format.fill = "#E2F0D9";
s.getRange("A13:D13").format = {
  fill: "#D9EAD3",
  font: { bold: true },
  borders: { preset: "all", style: "medium", color: "#93C47D" },
};
s.getRange("B10:C13").format.numberFormat = "0";
s.getRange("D10:D13").format.numberFormat = "0.000000";
s.getRange("A:A").format.columnWidth = 30;
s.getRange("B:D").format.columnWidth = 18;

const out = await SpreadsheetFile.exportXlsx(wb);
await out.save(path);
const preview = await wb.render({ sheetName: "Общий итог", range: "A1:D13", scale: 1.5, format: "png" });
await fs.writeFile("./output/summary_by_type.png", new Uint8Array(await preview.arrayBuffer()));
console.log((await wb.inspect({kind:"table",range:"Общий итог!A3:D13",include:"values,formulas",tableMaxRows:20,tableMaxCols:4})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"})).ndjson);
