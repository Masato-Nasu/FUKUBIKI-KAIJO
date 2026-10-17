export function syncRemainder(prizes,total,createId=()=>crypto.randomUUID()){
 if(!Number.isSafeInteger(total)||total<0||total>0xffffffff)throw Error('玉の総数は0〜4,294,967,295個の整数にしてください');
 const existing=prizes.filter(p=>p.isRemainder===true);if(existing.length>1)throw Error('残りの玉の設定が重複しています');
 const assigned=prizes.filter(p=>!p.isRemainder).reduce((n,p)=>n+p.initialCount,0);
 if(!Number.isSafeInteger(assigned)||assigned<0)throw Error('景品の本数を確認してください');
 if(assigned>total)throw Error('景品が玉の総数を'+(assigned-total)+'本超えています。総数を増やすか、景品の本数を減らしてください');
 let remainder=existing[0];const count=total-assigned,used=remainder?remainder.initialCount-remainder.remaining:0;
 if(count<used)throw Error('抽選済みの玉を含めると総数が足りません。総数を増やしてください');
 if(!remainder){remainder={id:createId(),isRemainder:true,grade:'はずれ',name:'はずれ',color:'#f4efe2',kind:'lose',effect:'auto',startsAt:1,initialCount:0,remaining:0};prizes.push(remainder)}
 remainder.initialCount=count;remainder.remaining=count-used;remainder.startsAt=1;return remainder;
}
export function checkCapacity(s){if(s.ballTotal===undefined)return;const count=s.prizes.reduce((n,p)=>n+p.initialCount,0);if(!Number.isSafeInteger(s.ballTotal)||s.ballTotal<0||s.ballTotal>0xffffffff||count!==s.ballTotal)throw Error('玉の総数と景品・残りの玉の合計が一致しません');if(s.prizes.filter(p=>p.isRemainder===true).length>1)throw Error('残りの玉の設定が重複しています')}
