import fs from "node:fs/promises";
import { Workbook, SpreadsheetFile } from "@oai/artifact-tool";

const outDir = "C:/Users/user/Documents/«Гермес Клин»/04_drafts/order001_corrected";
await fs.mkdir(outDir, { recursive: true });

const wb = Workbook.create();
const summary = wb.worksheets.add("КРАТКИЙ ИТОГ");
const full = wb.worksheets.add("ПОЛНЫЙ ЗАКАЗ");
const order = wb.worksheets.add("Заказ");
const details = wb.worksheets.add("Детали");
const finance = wb.worksheets.add("Финансы");
const check = wb.worksheets.add("Сверка");

for (const s of [summary, full, order, details, finance, check]) s.showGridLines = false;

summary.getRange("A1:D1").merge();
summary.getRange("A1").values=[["ЗАКАЗ №001 — АЛЕКСЕЙ, ДВЕРИ"]];
summary.getRange("A3:B8").values=[
  ["Материал","МДФ"],["Цвет","NCS S 1000-N"],["Блеск","10%"],
  ["Работа","Только покраска"],["Статус","Выполнен, оплачен полностью"],["Работники","Шкурщик и маляр"],
];
summary.getRange("A10:D10").values=[["Позиция","Квадратура / объём","Цена за единицу","Сумма"]];
summary.getRange("A11:D13").values=[
  ["Коробки и доборы","25 м²",18000,450000],
  ["Полотна, две стороны ×2","32 м²",25000,800000],
  ["Фрезерованные наличники","116 пог. м",3000,348000],
];
summary.getRange("A14:C14").merge(); summary.getRange("A14").values=[["Итого по позициям"]]; summary.getRange("D14").formulas=[["=SUM(D11:D13)"]];
summary.getRange("A15:C15").merge(); summary.getRange("A15").values=[["Округление"]]; summary.getRange("D15").formulas=[["=D16-D14"]];
summary.getRange("A16:C16").merge(); summary.getRange("A16").values=[["Получено от клиента"]]; summary.getRange("D16").values=[[1600000]];
summary.getRange("A18:D18").merge(); summary.getRange("A18").values=[["РАСХОДЫ И ПРИБЫЛЬ"]];
summary.getRange("A19:C19").values=[["Расход","Количество / расчёт","Сумма"]];
summary.getRange("A20:C28").values=[
  ["Шкурщик","616 000 ÷ 2",308000],["Маляр","616 000 ÷ 2",308000],
  ["Всего оплата работникам","308 000 + 308 000",null],
  ["Грунт","50 кг × 5 000 ₸",250000],["Краска","25 кг × 12 000 ₸",300000],
  ["Условная аренда","—",150000],["Налог ИП","4% × 1 600 000 ₸",null],
  ["Всего расходов","",null],["Чистая прибыль","1 600 000 − расходы",null],
];
summary.getRange("C22").formulas=[["=SUM(C20:C21)"]];
summary.getRange("C26").formulas=[["=D16*4%"]];
summary.getRange("C27").formulas=[["=SUM(C20:C21,C23:C26)"]];
summary.getRange("C28").formulas=[["=D16-C27"]];

order.getRange("A1:F1").merge();
order.getRange("A1").values = [["Заказ №001 — Алексей, двери"]];
order.getRange("A3:B12").values = [
  ["Дата учёта", new Date("2026-07-15")],
  ["Статус", "Выполнен, оплачен полностью"],
  ["Тип работы", "Только покраска; детали получены готовыми"],
  ["Материал", "МДФ; толщина для этого заказа не указывается"],
  ["Цвет", "NCS S 1000-N"],
  ["Блеск", "10%"],
  ["Торцы", "Не учитываются"],
  ["Коробки и доборы", "Одна окрашиваемая сторона"],
  ["Полотна", "Две стороны (×2)"],
  ["Источник итогов", "Подтверждение владельца + итоговый рукописный лист"],
];
order.getRange("A14:D14").values = [["Группа", "Расчётный объём", "Ставка, ₸", "Договорная сумма, ₸"]];
order.getRange("A15:D17").values = [
  ["Коробки + доборы", 25, 18000, 450000],
  ["Полотна ×2", 32, 25000, 800000],
  ["Фрезерованные наличники", 116, 3000, 348000],
];
order.getRange("A18:C18").merge(); order.getRange("A18").values = [["Итого по позициям"]];
order.getRange("D18").formulas = [["=SUM(D15:D17)"]];
order.getRange("A19:C19").merge(); order.getRange("A19").values = [["Согласованная сумма заказа"]];
order.getRange("D19").values = [[1600000]];
order.getRange("A20:C20").merge(); order.getRange("A20").values = [["Округление / скидка"]];
order.getRange("D20").formulas = [["=D19-D18"]];
order.getRange("A22:F24").merge();
order.getRange("A22").values = [["Важно: 25 м², 32 м² и 116 пог. м — подтверждённые коммерческие итоги. Детальные размеры ниже используются для сверки; они не должны молча заменять согласованные значения."]];

const rows = [
  ["Коробки","Коробка",1000,168,10,1,18000,"Фото/цифровой список"],
  ["Коробки","Коробка",2150,168,20,1,18000,"Фото/цифровой список"],
  ["Полотна","Полотно",2272,804,1,2,25000,"Цифровой список; сверить с фото"],
  ["Полотна","Полотно",2272,674,1,2,25000,"Цифровой список; сверить с фото"],
  ["Полотна","Полотно",2272,644,1,2,25000,"Цифровой список; сверить с фото"],
  ...Array.from({length:4},()=>["Полотна","Полотно",2000,814,1,2,25000,"Цифровой список"]),
  ["Полотна","Полотно",1992,814,1,2,25000,"Цифровой список; рукопись неясна"],
  ...Array.from({length:2},()=>["Полотна","Полотно",2000,814,1,2,25000,"Цифровой список"]),
  ["Доборы","Добор",2370,340,2,1,18000,"Комплект 1, боковые"],["Доборы","Добор",980,340,1,1,18000,"Комплект 1, верхняя"],
  ["Доборы","Добор",2370,340,2,1,18000,"Комплект 2, боковые"],["Доборы","Добор",850,340,1,1,18000,"Комплект 2, верхняя"],
  ["Доборы","Добор",2370,190,2,1,18000,"Комплект 3, боковые"],["Доборы","Добор",820,190,1,1,18000,"Комплект 3, верхняя"],
  ["Доборы","Добор",2120,360,2,1,18000,"Комплект 4, боковые"],["Доборы","Добор",1000,360,1,1,18000,"Комплект 4, верхняя"],
  ["Доборы","Добор",2120,330,2,1,18000,"Комплект 5, боковые"],["Доборы","Добор",1000,330,1,1,18000,"Комплект 5, верхняя"],
  ["Доборы","Добор",2120,340,2,1,18000,"Комплект 6, боковые"],["Доборы","Добор",1000,340,1,1,18000,"Комплект 6, верхняя"],
  ["Доборы","Добор",2120,340,2,1,18000,"Комплект 7, боковые"],["Доборы","Добор",1000,340,1,1,18000,"Комплект 7, верхняя"],
  ["Доборы","Добор",2120,190,2,1,18000,"Комплект 8, боковые"],["Доборы","Добор",1000,190,1,1,18000,"Комплект 8, верхняя"],
  ["Доборы","Добор",2120,340,2,1,18000,"Комплект 9, боковые"],["Доборы","Добор",1000,340,1,1,18000,"Комплект 9, верхняя"],
  ["Доборы","Добор",2120,290,2,1,18000,"Комплект 10, боковые"],["Доборы","Добор",1000,290,1,1,18000,"Комплект 10, верхняя"],
];

full.getRange("A1:K1").merge();
full.getRange("A1").values=[["ЗАКАЗ №001 — АЛЕКСЕЙ, ДВЕРИ — ПОЛНЫЙ ДОКУМЕНТ"]];
full.getRange("A3:B12").values=[
  ["Дата учёта",new Date("2026-07-15")],["Статус","Выполнен; клиент оплатил полностью"],
  ["Работа","Только покраска; детали получены готовыми и фрезерованными"],
  ["Материал","МДФ; толщина в этом заказе не указывается"],["Цвет","NCS S 1000-N"],["Блеск","10%"],
  ["Торцы","Не учитываются"],["Прямые детали","Одна сторона; модерн"],["Полотна","Две стороны (×2)"],
  ["Примечание","Цифровые размеры сверяются с исходными фотографиями"],
];
full.getRange("A14:K14").merge(); full.getRange("A14").values=[["ВСЕ РАЗМЕРЫ И ТЕХНИЧЕСКИЙ РАСЧЁТ"]];
full.getRange("A15:K15").values=[["№","Группа","Деталь","Высота, мм","Ширина, мм","Кол-во","Сторон","Площадь, м²","Ставка, ₸","Техническая сумма, ₸","Примечание"]];
full.getRange(`A16:K${15+rows.length}`).values=rows.map((r,i)=>[i+1,...r.slice(0,6),null,r[6],null,r[7]]);
full.getRange("H16").formulas=[["=D16*E16*F16*G16/1000000"]]; full.getRange(`H16:H${15+rows.length}`).fillDown();
full.getRange("J16").formulas=[["=H16*I16"]]; full.getRange(`J16:J${15+rows.length}`).fillDown();
let rr=17+rows.length;
full.getRange(`A${rr}:G${rr}`).merge(); full.getRange(`A${rr}`).values=[["Технический итог по деталям"]];
full.getRange(`H${rr}`).formulas=[[`=SUM(H16:H${15+rows.length})`]]; full.getRange(`J${rr}`).formulas=[[`=SUM(J16:J${15+rows.length})`]];
rr+=2; full.getRange(`A${rr}:K${rr}`).merge(); full.getRange(`A${rr}`).values=[["НАЛИЧНИКИ — ПОГОННЫЕ МЕТРЫ"]];
rr++; full.getRange(`A${rr}:F${rr}`).values=[["Позиция","Длина, м","Количество","Итого, пог. м","Ставка, ₸/м","Сумма, ₸"]];
const trimStart=rr+1;
full.getRange(`A${trimStart}:F${trimStart+4}`).values=[
  ["Наличник",2.25,32,null,3000,null],
  ["Наличник",2.45,14,null,3000,null],
  ["Наличник",2.04,3,null,3000,null],
  ["Наличник",1.855,1,null,3000,null],
  ["Неучтённые мелкие детали",1.725,1,null,3000,null],
];
full.getRange(`D${trimStart}`).formulas=[[`=B${trimStart}*C${trimStart}`]]; full.getRange(`D${trimStart}:D${trimStart+4}`).fillDown();
full.getRange(`F${trimStart}`).formulas=[[`=D${trimStart}*E${trimStart}`]]; full.getRange(`F${trimStart}:F${trimStart+4}`).fillDown();
const trimTotal=trimStart+5;
full.getRange(`A${trimTotal}:C${trimTotal}`).merge(); full.getRange(`A${trimTotal}`).values=[["Итого наличники"]];
full.getRange(`D${trimTotal}`).formulas=[[`=SUM(D${trimStart}:D${trimStart+4})`]]; full.getRange(`F${trimTotal}`).formulas=[[`=SUM(F${trimStart}:F${trimStart+4})`]];
rr=trimTotal+2; full.getRange(`A${rr}:K${rr}`).merge(); full.getRange(`A${rr}`).values=[["ПОДТВЕРЖДЁННЫЙ КОММЕРЧЕСКИЙ РАСЧЁТ"]];
rr++; full.getRange(`A${rr}:D${rr}`).values=[["Позиция","Объём","Ставка, ₸","Сумма, ₸"]];
const commercialStart=rr+1;
full.getRange(`A${commercialStart}:D${commercialStart+2}`).values=[
  ["Коробки + доборы",25,18000,450000],["Полотна ×2",32,25000,800000],["Фрезерованные наличники, пог. м",116,3000,348000]
];
let ctot=commercialStart+3; full.getRange(`A${ctot}:C${ctot}`).merge(); full.getRange(`A${ctot}`).values=[["Итого по позициям"]]; full.getRange(`D${ctot}`).formulas=[[`=SUM(D${commercialStart}:D${commercialStart+2})`]];
ctot++; full.getRange(`A${ctot}:C${ctot}`).merge(); full.getRange(`A${ctot}`).values=[["Согласованная сумма заказа"]]; full.getRange(`D${ctot}`).values=[[1600000]];
ctot++; full.getRange(`A${ctot}:C${ctot}`).merge(); full.getRange(`A${ctot}`).values=[["Округление к согласованной сумме"]]; full.getRange(`D${ctot}`).formulas=[[`=D${ctot-1}-D${ctot-2}`]];
ctot++; full.getRange(`A${ctot}:C${ctot}`).merge(); full.getRange(`A${ctot}`).values=[["Автоматическая проверка"]];
full.getRange(`D${ctot}`).formulas=[[`=IF(AND(D${trimTotal}=116,D${ctot-2}=1600000),"ПРОВЕРЕНО","ОШИБКА")`]];
let fr=ctot+2; full.getRange(`A${fr}:K${fr}`).merge(); full.getRange(`A${fr}`).values=[["МАТЕРИАЛЫ, РАСХОДЫ И ПРИБЫЛЬ"]];
fr++; full.getRange(`A${fr}:C${fr}`).values=[["Статья","Сумма, ₸","Статус / пояснение"]];
const fstart=fr+1;
full.getRange(`A${fstart}:C${fstart+8}`).values=[
  ["Выручка",1600000,"Получено полностью"],["Шкурщик",308000,"Оплачено"],["Маляр",308000,"Оплачено"],
  ["Всего оплата работникам",null,"Контрольный итог"],
  ["Грунт: 50 кг × 5 000",250000,"Куплен и потрачен"],["Краска: 25 кг × 12 000",300000,"Куплена и потрачена"],
  ["Условная аренда",150000,"Приблизительно для этого заказа"],["Налог ИП 4%",null,"Уплачен"],["Чистая прибыль",null,"После всех указанных расходов"]
];
full.getRange(`B${fstart+3}`).formulas=[[`=SUM(B${fstart+1}:B${fstart+2})`]];
full.getRange(`B${fstart+7}`).formulas=[[`=B${fstart}*4%`]];
full.getRange(`B${fstart+8}`).formulas=[[`=B${fstart}-SUM(B${fstart+1}:B${fstart+2},B${fstart+4}:B${fstart+7})`]];
details.getRange("A1:J1").values = [["№","Группа","Деталь","Высота, мм","Ширина, мм","Кол-во","Коэф. сторон","Площадь, м²","Ставка, ₸","Источник / примечание"]];
details.getRange(`A2:J${rows.length+1}`).values = rows.map((r,i)=>[i+1,...r.slice(0,6),null,r[6],r[7]]);
details.getRange("H2").formulas = [["=D2*E2*F2*G2/1000000"]];
details.getRange(`H2:H${rows.length+1}`).fillDown();
details.getRange(`A${rows.length+3}:G${rows.length+3}`).merge(); details.getRange(`A${rows.length+3}`).values=[["Техническая площадь по детальному списку"]];
details.getRange(`H${rows.length+3}`).formulas=[[`=SUM(H2:H${rows.length+1})`]];

finance.getRange("A1:D1").merge(); finance.getRange("A1").values=[["Финансы заказа №001"]];
finance.getRange("A3:C3").values=[["Статья","Сумма, ₸","Статус / пояснение"]];
finance.getRange("A4:C12").values=[
  ["Выручка",1600000,"Получено полностью"],["Шкурщик",308000,"Оплачено"],["Маляр",308000,"Оплачено"],
  ["Всего оплата работникам",null,"Контрольный итог"],
  ["Грунт: 50 кг × 5 000",250000,"Фактически куплен и потрачен"],
  ["Краска: 25 кг × 12 000",300000,"Фактически куплена и потрачена"],
  ["Условная аренда",150000,"Оценка только для этого заказа"],
  ["Налог ИП 4%",null,"Уплачен; 4% от выручки"],["Чистая прибыль",null,"После указанных расходов и налога"],
];
finance.getRange("B7").formulas=[["=SUM(B5:B6)"]]; finance.getRange("B11").formulas=[["=B4*4%"]];
finance.getRange("B12").formulas=[["=B4-SUM(B5:B6,B8:B11)"]];

check.getRange("A1:E1").values=[["Показатель","Черновые размеры","Подтверждено","Разница","Решение"]];
check.getRange("A2:E4").values=[
  ["Коробки + доборы, м²",null,25,null,"Использовать подтверждённые 25 м²"],
  ["Полотна ×2, м²",null,32,null,"Использовать подтверждённые 32 м²"],
  ["Наличники, пог. м",114.275,116,null,"Добавить 1,725 м неучтённых деталей"],
];
check.getRange("B2").formulas=[[`=SUMIF('Детали'!B2:B${rows.length+1},"Коробки",'Детали'!H2:H${rows.length+1})+SUMIF('Детали'!B2:B${rows.length+1},"Доборы",'Детали'!H2:H${rows.length+1})`]];
check.getRange("B3").formulas=[[`=SUMIF('Детали'!B2:B${rows.length+1},"Полотна",'Детали'!H2:H${rows.length+1})`]];
check.getRange("D2").formulas=[["=C2-B2"]]; check.getRange("D2:D4").fillDown();

const titleFmt={fill:"#1F4E78",font:{bold:true,color:"#FFFFFF",size:16},verticalAlignment:"center"};
const headerFmt={fill:"#D9EAF7",font:{bold:true,color:"#17365D"},borders:{preset:"inside",style:"thin",color:"#AAB7C4"}};
for(const [s,r] of [[summary,"A1:D1"],[full,"A1:K1"],[order,"A1:F1"],[finance,"A1:D1"]]) s.getRange(r).format=titleFmt;
for(const [s,r] of [[summary,"A10:D10"],[summary,"A19:C19"],[full,"A15:K15"],[order,"A14:D14"],[details,"A1:J1"],[finance,"A3:C3"],[check,"A1:E1"]]) s.getRange(r).format=headerFmt;
summary.getRange("A18:D18").format={fill:"#5B9BD5",font:{bold:true,color:"#FFFFFF"}};
summary.getRange("C11:D16").format.numberFormat="#,##0 [$₸-kk-KZ]"; summary.getRange("C20:C28").format.numberFormat="#,##0 [$₸-kk-KZ]";
summary.getRange("A14:D16").format.font={bold:true}; summary.getRange("A22:C22").format.font={bold:true}; summary.getRange("A27:C28").format.font={bold:true};
for(const r of [`A14:K14`,`A${17+rows.length+2}:K${17+rows.length+2}`,`A${trimTotal+2}:K${trimTotal+2}`,`A${fr}:K${fr}`]) full.getRange(r).format={fill:"#5B9BD5",font:{bold:true,color:"#FFFFFF"}};
full.getRange("B3").format.numberFormat="yyyy-mm-dd";
full.getRange(`H16:J${15+rows.length}`).format.numberFormat="#,##0.000";
full.getRange(`B${trimStart}:D${trimTotal}`).format.numberFormat="0.000";
full.getRange(`E${trimStart}:F${trimTotal}`).format.numberFormat="#,##0 [$₸-kk-KZ]";
full.getRange(`C${commercialStart}:D${ctot}`).format.numberFormat="#,##0 [$₸-kk-KZ]";
full.getRange(`B${fstart}:B${fstart+8}`).format.numberFormat="#,##0 [$₸-kk-KZ]";
order.getRange("A22:F24").format={fill:"#FFF2CC",font:{italic:true,color:"#7F6000"},wrapText:true};
order.getRange("B3").format.numberFormat="yyyy-mm-dd";
order.getRange("C15:D20").format.numberFormat="#,##0 [$₸-kk-KZ]";
details.getRange(`H2:I${rows.length+3}`).format.numberFormat="#,##0.000";
finance.getRange("B4:B12").format.numberFormat="#,##0 [$₸-kk-KZ]";
check.getRange("B2:D4").format.numberFormat="0.000";
for(const s of [summary,full,order,details,finance,check]) { const u=s.getUsedRange(); u.format.autofitColumns(); u.format.autofitRows(); }
summary.getRange("A1:D28").format.wrapText=true; summary.getRange("A1:A28").format.columnWidth=32; summary.getRange("B1:B28").format.columnWidth=24; summary.getRange("C1:D28").format.columnWidth=20;
full.getRange(`K1:K${fstart+6}`).format.columnWidth=34; full.getRange(`K1:K${fstart+6}`).format.wrapText=true; full.freezePanes.freezeRows(15);
order.getRange("A1:F24").format.wrapText=true; details.getRange(`J1:J${rows.length+1}`).format.columnWidth=34; details.getRange(`J1:J${rows.length+1}`).format.wrapText=true;
details.freezePanes.freezeRows(1); finance.freezePanes.freezeRows(3); check.freezePanes.freezeRows(1);

const errors=await wb.inspect({kind:"match",searchTerm:"#REF!|#DIV/0!|#VALUE!|#NAME\\?|#N/A",options:{useRegex:true,maxResults:100},summary:"formula errors"});
console.log(errors.ndjson);
for(const name of ["КРАТКИЙ ИТОГ","ПОЛНЫЙ ЗАКАЗ","Заказ","Детали","Финансы","Сверка"]){const png=await wb.render({sheetName:name,autoCrop:"all",scale:1,format:"png"}); await fs.writeFile(`${outDir}/${name}.png`,new Uint8Array(await png.arrayBuffer()));}
const xlsx=await SpreadsheetFile.exportXlsx(wb); await xlsx.save(`${outDir}/Заказ_001_Алексей_последняя_правка.xlsx`);
