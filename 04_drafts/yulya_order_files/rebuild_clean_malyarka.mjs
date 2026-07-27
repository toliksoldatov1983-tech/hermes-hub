import fs from "node:fs/promises";
import { SpreadsheetFile, Workbook } from "@oai/artifact-tool";

const outputPath = "./output/Юля_фасады_выборка_90_Малярка.xlsx";
const rows = [
  ["6010","Выборка",608,598,4,""],["6010","Выборка",442,598,1,""],["6010","Выборка",358,598,1,""],["6010","Выборка",718,598,2,""],["6010","Выборка",1068,598,2,""],["6010","Выборка",1028,598,1,""],["6010","Выборка",718,198,2,""],["6010","Выборка",358,858,1,""],["6010","Выборка",178,858,2,""],
  ["6010","Модерн",147,200,1,""],["6010","Модерн",147,2510,1,""],["6010","Модерн",147,700,1,""],["6010","Модерн",1680,20,1,""],["6010","Модерн",105,1300,1,""],["6010","Модерн",105,1250,1,""],["6010","Модерн",105,650,2,""],["6010","Модерн",718,44,1,""],["6010","Модерн",600,40,1,""],
  ["1000","Выборка",718,448,4,""],["1000","Выборка",718,598,3,""],["1000","Выборка",718,553,1,""],["1000","Выборка",358,898,2,""],["1000","Выборка",178,898,4,""],["1000","Выборка",358,598,2,""],
  ["1000","Модерн",718,50,1,""],["1000","Модерн",718,100,1,""],["1000","Модерн",147,2750,1,""],["1000","Модерн",147,2700,1,""],["1000","Модерн",147,1250,1,""],
  ["6010","Витрина",498,498,3,""],
  ["6010","Витрина",1628,498,3,"Выборка под стекло с задней стороны: глубина 10 мм, отступ от наружного края 20 мм."],
  ["6010","Модерн",2230,450,2,"Подкрас с обратной стороны: 100 мм по одной длине."],
  ["6010","Модерн",97,1500,1,""]
];
const fills={"Выборка":"#FFF2CC","Модерн":"#DDEBF7","Витрина":"#E2F0D9"};
const wb=Workbook.create();
const summary=wb.worksheets.add("Общий итог");
const s6010=wb.worksheets.add("6010-R90B");
const s1000=wb.worksheets.add("1000-N");

function buildColorSheet(s,data,ncs){
  s.showGridLines=false;
  s.mergeCells("A1:I1");
  s.getRange("A1").values=[[`Юля, фасады, выборка 90 градусов — ${ncs}`]];
  s.getRange("A1:I1").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:16},horizontalAlignment:"center"};
  s.getRange("A3:B6").values=[["Материал","МДФ 16 мм"],["Расчёт","Одна лицевая плоскость"],["Количество деталей",null],["Общая площадь, м²",null]];
  const start=9,end=start+data.length-1;
  s.getRange("B5").formulas=[[`=SUM(F${start}:F${end})`]];
  s.getRange("B6").formulas=[[`=SUM(H${start}:H${end})`]];
  s.getRange("A3:B6").format.borders={preset:"all",style:"thin",color:"#8EA9C1"};
  s.getRange("A5:B6").format={fill:"#D9EAF7",font:{bold:true}};
  s.mergeCells("D2:H2");s.getRange("D2").values=[["ВЕСЬ ЗАКАЗ"]];
  s.getRange("D2:H2").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:12},horizontalAlignment:"center"};
  for(const r of [3,4,5,6,7])s.mergeCells(`D${r}:G${r}`);
  s.getRange("D3:D7").values=[["Общее количество деталей"],["Общая квадратура, м²"],["Фрезерованная выборка, м²"],["Модерн, м²"],["Витрина, м²"]];
  s.getRange("H3:H7").formulas=[["='Общий итог'!C6"],["='Общий итог'!D6"],["='Общий итог'!D10"],["='Общий итог'!D11"],["='Общий итог'!D12"]];
  s.getRange("D3:H7").format={fill:"#EAF2F8",borders:{preset:"all",style:"thin",color:"#8EA9C1"}};
  s.getRange("D3:D7").format.font={bold:true};
  s.getRange("H3:H7").format={fill:"#D9EAD3",font:{bold:true},horizontalAlignment:"right",borders:{preset:"all",style:"thin",color:"#93C47D"}};
  s.getRange("H3").format.numberFormat="0";s.getRange("H4:H7").format.numberFormat="0.000000";
  s.getRange("A8:I8").values=[["№","Тип","Высота, мм","Ширина, мм","Толщина, мм","Количество","м² за 1 шт.","Всего, м²","Примечание"]];
  s.getRange("A8:I8").format={fill:"#4472C4",font:{bold:true,color:"#FFFFFF"},horizontalAlignment:"center",wrapText:true,borders:{preset:"all",style:"thin",color:"#D9E2F3"}};
  s.getRange(`A${start}:F${end}`).values=data.map((r,i)=>[i+1,r[1],r[2],r[3],16,r[4]]);
  s.getRange(`I${start}:I${end}`).values=data.map(r=>[r[5]]);
  data.forEach((r,i)=>{const q=start+i;s.getRange(`G${q}`).formulas=[[`=C${q}*D${q}/1000000`]];s.getRange(`H${q}`).formulas=[[`=G${q}*F${q}`]];s.getRange(`A${q}:I${q}`).format={fill:fills[r[1]],borders:{insideHorizontal:{style:"thin",color:"#D9D9D9"}},verticalAlignment:"center"};});
  s.getRange(`C${start}:F${end}`).format.numberFormat="0";s.getRange(`G${start}:H${end}`).format.numberFormat="0.000000";s.getRange(`A${start}:H${end}`).format.horizontalAlignment="center";s.getRange(`I${start}:I${end}`).format.wrapText=true;
  s.getRange(`A${end+2}:B${end+3}`).values=[["Итого деталей",null],["Итого площадь, м²",null]];s.getRange(`B${end+2}`).formulas=[[`=SUM(F${start}:F${end})`]];s.getRange(`B${end+3}`).formulas=[[`=SUM(H${start}:H${end})`]];s.getRange(`A${end+2}:B${end+3}`).format={fill:"#D9EAD3",font:{bold:true},borders:{preset:"all",style:"thin",color:"#93C47D"}};s.getRange(`B${end+3}`).format.numberFormat="0.000000";
  [18,16,13,13,13,12,14,14,52].forEach((w,i)=>s.getRangeByIndexes(0,i,end+4,1).format.columnWidth=w);s.getRange(`8:${end}`).format.rowHeight=30;s.freezePanes.freezeRows(8);
}
buildColorSheet(s6010,rows.filter(r=>r[0]==="6010"),"NCS S 6010-R90B");
buildColorSheet(s1000,rows.filter(r=>r[0]==="1000"),"NCS S 1000-N");

summary.showGridLines=false;summary.mergeCells("A1:D1");summary.getRange("A1").values=[["Юля, фасады, выборка 90 градусов — общий итог"]];summary.getRange("A1:D1").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:16},horizontalAlignment:"center"};
summary.getRange("A3:D6").values=[["Цвет","Размерных строк","Деталей","Площадь, м²"],["NCS S 6010-R90B",22,null,null],["NCS S 1000-N",11,null,null],["Весь заказ",33,null,null]];
summary.getRange("C4:D4").formulas=[["='6010-R90B'!B5","='6010-R90B'!B6"]];summary.getRange("C5:D5").formulas=[["='1000-N'!B5","='1000-N'!B6"]];summary.getRange("C6:D6").formulas=[["=SUM(C4:C5)","=SUM(D4:D5)"]];
summary.mergeCells("A8:D8");summary.getRange("A8").values=[["Итог по типу деталей"]];summary.getRange("A8:D8").format={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:13},horizontalAlignment:"center"};
summary.getRange("A9:D13").values=[["Тип","Размерных строк","Деталей","Площадь, м²"],["Фрезерованная выборка",null,null,null],["Модерн",null,null,null],["Витрина",null,null,null],["Весь заказ",null,null,null]];
for(const [r,t] of [[10,"Выборка"],[11,"Модерн"],[12,"Витрина"]]){summary.getRange(`B${r}`).formulas=[[`=COUNTIF('6010-R90B'!B9:B30,\"${t}\")+COUNTIF('1000-N'!B9:B19,\"${t}\")`]];summary.getRange(`C${r}`).formulas=[[`=SUMIF('6010-R90B'!B9:B30,\"${t}\",'6010-R90B'!F9:F30)+SUMIF('1000-N'!B9:B19,\"${t}\",'1000-N'!F9:F19)`]];summary.getRange(`D${r}`).formulas=[[`=SUMIF('6010-R90B'!B9:B30,\"${t}\",'6010-R90B'!H9:H30)+SUMIF('1000-N'!B9:B19,\"${t}\",'1000-N'!H9:H19)`]];}
summary.getRange("B13:D13").formulas=[["=SUM(B10:B12)","=SUM(C10:C12)","=SUM(D10:D12)"]];
for(const range of ["A3:D3","A9:D9"])summary.getRange(range).format={fill:"#4472C4",font:{bold:true,color:"#FFFFFF"},horizontalAlignment:"center",borders:{preset:"all",style:"thin",color:"#D9E2F3"}};
summary.getRange("A4:D5").format.borders={preset:"all",style:"thin",color:"#D9D9D9"};summary.getRange("A10:D12").format.borders={preset:"all",style:"thin",color:"#D9D9D9"};summary.getRange("A10:D10").format.fill="#FFF2CC";summary.getRange("A11:D11").format.fill="#DDEBF7";summary.getRange("A12:D12").format.fill="#E2F0D9";
for(const range of ["A6:D6","A13:D13"])summary.getRange(range).format={fill:"#D9EAD3",font:{bold:true},borders:{preset:"all",style:"medium",color:"#93C47D"}};
summary.getRange("B4:C13").format.numberFormat="0";summary.getRange("D4:D13").format.numberFormat="0.000000";summary.getRange("A:A").format.columnWidth=30;summary.getRange("B:D").format.columnWidth=18;

const out=await SpreadsheetFile.exportXlsx(wb);await out.save(outputPath);
for(const [sn,fn,rg] of [["Общий итог","clean_summary.png","A1:D13"],["6010-R90B","clean_6010.png","A1:I31"],["1000-N","clean_1000.png","A1:I20"]]){const b=await wb.render({sheetName:sn,range:rg,scale:1,format:"png"});await fs.writeFile(`./output/${fn}`,new Uint8Array(await b.arrayBuffer()));}
console.log((await wb.inspect({kind:"table",range:"Общий итог!A3:D13",include:"values,formulas",tableMaxRows:20,tableMaxCols:4})).ndjson);
console.log((await wb.inspect({kind:"table",range:"6010-R90B!A8:I30",include:"values,formulas",tableMaxRows:30,tableMaxCols:9,tableMaxCellChars:140})).ndjson);
console.log((await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"})).ndjson);
