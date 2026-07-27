import fs from "node:fs/promises";
import { FileBlob, SpreadsheetFile } from "@oai/artifact-tool";

const path="./output/Юля_фасады_выборка_90_Малярка.xlsx";
const wb=await SpreadsheetFile.importXlsx(await FileBlob.load(path));
const s=wb.worksheets.getItem("Общий итог");
s.unmergeCells("A1:D1");s.mergeCells("A1:E1");

s.mergeCells("A15:E15");s.getRange("A15").values=[["СТОИМОСТЬ РАБОТ"]];
s.getRange("A15:E15").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:13},horizontalAlignment:"center"};
s.getRange("A16:E21").values=[
  ["Тип","Площадь, м²","Ставка, ₸/м²","Сумма, ₸","Статус"],
  ["Выборка 90°",null,33000,null,"Рассчитано"],
  ["Модерн",null,26000,null,"Рассчитано"],
  ["Витрина",null,null,null,"Ставка не задана"],
  ["Итого по заданным ставкам",null,null,null,"Без стоимости витрин"],
  ["Полная стоимость заказа",null,null,null,"Ожидается ставка витрин"]
];
s.getRange("B17").formulas=[["=D10"]];s.getRange("B18").formulas=[["=D11"]];s.getRange("B19").formulas=[["=D12"]];
s.getRange("D17").formulas=[["=B17*C17"]];s.getRange("D18").formulas=[["=B18*C18"]];
s.getRange("D20").formulas=[["=SUM(D17:D18)"]];
s.getRange("A16:E16").format={fill:"#4472C4",font:{bold:true,color:"#FFFFFF"},horizontalAlignment:"center",borders:{preset:"all",style:"thin",color:"#D9E2F3"}};
s.getRange("A17:E19").format.borders={preset:"all",style:"thin",color:"#D9D9D9"};s.getRange("A17:E17").format.fill="#FFF2CC";s.getRange("A18:E18").format.fill="#DDEBF7";s.getRange("A19:E19").format.fill="#E2F0D9";
s.getRange("A20:E20").format={fill:"#D9EAD3",font:{bold:true},borders:{preset:"all",style:"medium",color:"#93C47D"}};
s.getRange("A21:E21").format={fill:"#FCE8E6",font:{bold:true,color:"#9C0006"},borders:{preset:"all",style:"thin",color:"#E6B8AF"}};
s.getRange("B17:B19").format.numberFormat="0.000000";s.getRange("C17:D21").format.numberFormat='#,##0.00 "₸"';

s.mergeCells("A23:E23");s.getRange("A23").values=[["МАТЕРИАЛЫ — ДАННЫЕ ДЛЯ РАСЧЁТА"]];
s.getRange("A23:E23").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:13},horizontalAlignment:"center"};
s.getRange("A24:E29").values=[
  ["Материал","Основа","Норма / пропорция","Потребность","Статус"],
  ["Грунт","17,678846 м²","Нет данных","Не рассчитано","Нужна норма кг/м² и число слоёв"],
  ["Краска","17,678846 м²","Нет данных","Не рассчитано","Нужна норма кг/м² и число слоёв"],
  ["Отвердитель","От массы состава","Нет данных","Не рассчитано","Нужна пропорция производителя"],
  ["Разбавитель","От массы состава","Нет данных","Не рассчитано","Нужна пропорция производителя"],
  ["МДФ 16 мм","17,678846 м² деталей","Нет данных","Не рассчитано","Нужен формат листа и карта раскроя"]
];
s.getRange("A24:E24").format={fill:"#4472C4",font:{bold:true,color:"#FFFFFF"},horizontalAlignment:"center",borders:{preset:"all",style:"thin",color:"#D9E2F3"}};
s.getRange("A25:E29").format={fill:"#FFF4CC",borders:{preset:"all",style:"thin",color:"#E6D690"}};s.getRange("C25:D29").format.font={bold:true,color:"#9C6500"};
s.getRange("A31:E32").merge(true);s.getRange("A31").values=[["Важно: найденные в проекте 50 кг грунта и 25 кг краски относятся к другому заказу и не использованы как норма для заказа «Юля»."],["Для завершения полной стоимости требуется ставка на витрины."]];
s.getRange("A31:E32").format={fill:"#F2F2F2",font:{italic:true,color:"#595959"},wrapText:true,borders:{preset:"outside",style:"thin",color:"#BFBFBF"}};
s.getRange("A:A").format.columnWidth=32;s.getRange("B:D").format.columnWidth=20;s.getRange("E:E").format.columnWidth=36;s.getRange("24:32").format.rowHeight=28;

const out=await SpreadsheetFile.exportXlsx(wb);await out.save(path);
const preview=await wb.render({sheetName:"Общий итог",range:"A1:E32",scale:1.2,format:"png"});await fs.writeFile("./output/pricing_materials_summary.png",new Uint8Array(await preview.arrayBuffer()));
console.log((await wb.inspect({kind:"table",range:"Общий итог!A15:E32",include:"values,formulas",tableMaxRows:30,tableMaxCols:5,tableMaxCellChars:130})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"})).ndjson);
