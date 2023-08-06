"use strict";(globalThis.webpackChunksuperset=globalThis.webpackChunksuperset||[]).push([[3375],{62276:(t,e,a)=>{a.d(e,{S:()=>o,M:()=>r});var n=a(11448),l=a(51995);const i=n.Z.RangePicker,o=(0,l.iK)(i)`
  border-radius: ${({theme:t})=>t.gridUnit}px;
`,r=n.Z},76697:(t,e,a)=>{a.d(e,{Z:()=>n});const n=a(19181).Z},82342:(t,e,a)=>{a.d(e,{Z:()=>d}),a(67294);var n=a(51995),l=a(11965),i=a(61988),o=a(9882),r=a(58593),s=a(49238),u=a(70163),c={name:"8wgs83",styles:"margin-bottom:0;position:relative"};const d=({name:t,label:e,description:a,validationErrors:d=[],renderTrigger:m=!1,rightNode:p,leftNode:h,onClick:Z,hovered:g=!1,tooltipOnClick:v=(()=>{}),warning:f,danger:y})=>{const{gridUnit:b,colors:C}=(0,n.Fg)();if(!e)return null;const w=(null==d?void 0:d.length)>0?"text-danger":"";return(0,l.tZ)("div",{className:"ControlHeader"},(0,l.tZ)("div",{className:"pull-left"},(0,l.tZ)(s.lX,{css:c},h&&(0,l.tZ)("span",null,h),(0,l.tZ)("span",{role:"button",tabIndex:0,onClick:Z,className:w,style:{cursor:Z?"pointer":""}},e)," ",f&&(0,l.tZ)("span",null,(0,l.tZ)(r.u,{id:"error-tooltip",placement:"top",title:f},(0,l.tZ)(u.Z.AlertSolid,{iconColor:C.alert.base,iconSize:"s"}))," "),y&&(0,l.tZ)("span",null,(0,l.tZ)(r.u,{id:"error-tooltip",placement:"top",title:y},(0,l.tZ)(u.Z.ErrorSolid,{iconColor:C.error.base,iconSize:"s"}))," "),(null==d?void 0:d.length)>0&&(0,l.tZ)("span",null,(0,l.tZ)(r.u,{id:"error-tooltip",placement:"top",title:null==d?void 0:d.join(" ")},(0,l.tZ)(u.Z.ErrorSolid,{iconColor:C.error.base,iconSize:"s"}))," "),g?(0,l.tZ)("span",{css:()=>l.iv`
          position: absolute;
          top: 50%;
          right: 0;
          padding-left: ${b}px;
          transform: translate(100%, -50%);
          white-space: nowrap;
        `},a&&(0,l.tZ)("span",null,(0,l.tZ)(o.V,{label:(0,i.t)("description"),tooltip:a,placement:"top",onClick:v})," "),m&&(0,l.tZ)("span",null,(0,l.tZ)(o.V,{label:(0,i.t)("bolt"),tooltip:(0,i.t)("Changing this control takes effect instantly"),placement:"top",icon:"bolt"})," ")):null)),p&&(0,l.tZ)("div",{className:"pull-right"},p),(0,l.tZ)("div",{className:"clearfix"}))}},73375:(t,e,a)=>{a.d(e,{Z:()=>Nt});var n=a(5872),l=a.n(n),i=a(67294),o=a(15926),r=a.n(o),s=a(31069),u=a(51995),c=a(61988),d=a(30381),m=a.n(d);const p=" : ",h=(t,e)=>t.replace("T00:00:00","")||(e?"-∞":"∞"),Z=(t,e)=>{const a=t.split(p);if(1===a.length)return t;const n=(e||["unknown","unknown"]).map((t=>"inclusive"===t?"≤":"<"));return`${h(a[0],!0)} ${n[0]} col ${n[1]} ${h(a[1])}`},g="previous calendar week",v="previous calendar month",f="previous calendar year",y=[{value:"Common",label:(0,c.t)("Last"),order:0},{value:"Calendar",label:(0,c.t)("Previous"),order:1},{value:"Custom",label:(0,c.t)("Custom"),order:2},{value:"Advanced",label:(0,c.t)("Advanced"),order:3},{value:"No filter",label:(0,c.t)("No filter"),order:4}],b=[{value:"Last day",label:(0,c.t)("last day"),order:0},{value:"Last week",label:(0,c.t)("last week"),order:1},{value:"Last month",label:(0,c.t)("last month"),order:2},{value:"Last quarter",label:(0,c.t)("last quarter"),order:3},{value:"Last year",label:(0,c.t)("last year"),order:4}],C=new Set(b.map((({value:t})=>t))),w=[{value:g,label:(0,c.t)("previous calendar week"),order:0},{value:v,label:(0,c.t)("previous calendar month"),order:1},{value:f,label:(0,c.t)("previous calendar year"),order:2}],E=new Set(w.map((({value:t})=>t))),D=[{value:"second",label:t=>(0,c.t)("Seconds %s",t)},{value:"minute",label:t=>(0,c.t)("Minutes %s",t)},{value:"hour",label:t=>(0,c.t)("Hours %s",t)},{value:"day",label:t=>(0,c.t)("Days %s",t)},{value:"week",label:t=>(0,c.t)("Weeks %s",t)},{value:"month",label:t=>(0,c.t)("Months %s",t)},{value:"quarter",label:t=>(0,c.t)("Quarters %s",t)},{value:"year",label:t=>(0,c.t)("Years %s",t)}],x=D.map(((t,e)=>({value:t.value,label:t.label((0,c.t)("Before")),order:e}))),N=D.map(((t,e)=>({value:t.value,label:t.label((0,c.t)("After")),order:e}))),S=[{value:"specific",label:(0,c.t)("Specific Date/Time"),order:0},{value:"relative",label:(0,c.t)("Relative Date/Time"),order:1},{value:"now",label:(0,c.t)("Now"),order:2},{value:"today",label:(0,c.t)("Midnight"),order:3}],$=S.slice(),T=new Set(["Last day","Last week","Last month","Last quarter","Last year"]),M=new Set([g,v,f]),A="YYYY-MM-DD[T]HH:mm:ss",V=m()().utc().startOf("day").subtract(7,"days").format(A),k=m()().utc().startOf("day").format(A),G=String.raw`\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d(?:\.\d+)?(?:(?:[+-]\d\d:\d\d)|Z)?`,R=String.raw`TODAY|NOW`,L=String.raw`[+-]?[1-9][0-9]*`,I=String.raw`YEAR|QUARTER|MONTH|WEEK|DAY|HOUR|MINUTE|SECOND`,X=RegExp(String.raw`^DATEADD\(DATETIME\("(${G}|${R})"\),\s(${L}),\s(${I})\)$`,"i"),Y=RegExp(String.raw`^${G}$|^${R}$`,"i"),U=["now","today"],z={sinceDatetime:V,sinceMode:"relative",sinceGrain:"day",sinceGrainValue:-7,untilDatetime:k,untilMode:"specific",untilGrain:"day",untilGrainValue:7,anchorMode:"now",anchorValue:"now"},F=["specific","today","now"],O=t=>"now"===t?m()().utc().startOf("second"):"today"===t?m()().utc().startOf("day"):m()(t),q=t=>O(t).format(A),J=t=>{const e=t.split(p);if(2===e.length){const[t,a]=e;if(Y.test(t)&&Y.test(a)){const e=U.includes(t)?t:"specific",n=U.includes(a)?a:"specific";return{customRange:{...z,sinceDatetime:t,untilDatetime:a,sinceMode:e,untilMode:n},matchedFlag:!0}}const n=t.match(X);if(n&&Y.test(a)&&t.includes(a)){const[t,e,l]=n.slice(1),i=U.includes(a)?a:"specific";return{customRange:{...z,sinceGrain:l,sinceGrainValue:parseInt(e,10),sinceDatetime:t,untilDatetime:t,sinceMode:"relative",untilMode:i},matchedFlag:!0}}const l=a.match(X);if(Y.test(t)&&l&&a.includes(t)){const[e,a,n]=[...l.slice(1)],i=U.includes(t)?t:"specific";return{customRange:{...z,untilGrain:n,untilGrainValue:parseInt(a,10),sinceDatetime:e,untilDatetime:e,untilMode:"relative",sinceMode:i},matchedFlag:!0}}if(n&&l){const[t,e,a]=[...n.slice(1)],[i,o,r]=[...l.slice(1)];if(t===i)return{customRange:{...z,sinceGrain:a,sinceGrainValue:parseInt(e,10),sinceDatetime:t,untilGrain:r,untilGrainValue:parseInt(o,10),untilDatetime:i,anchorValue:t,sinceMode:"relative",untilMode:"relative",anchorMode:"now"===t?"now":"specific"},matchedFlag:!0}}}return{customRange:z,matchedFlag:!1}},H=t=>{const{sinceDatetime:e,sinceMode:a,sinceGrain:n,sinceGrainValue:l,untilDatetime:i,untilMode:o,untilGrain:r,untilGrainValue:s,anchorValue:u}={...t};if(F.includes(a)&&F.includes(o))return`${"specific"===a?q(e):a} : ${"specific"===o?q(i):o}`;if(F.includes(a)&&"relative"===o){const t="specific"===a?q(e):a;return`${t} : DATEADD(DATETIME("${t}"), ${s}, ${r})`}if("relative"===a&&F.includes(o)){const t="specific"===o?q(i):o;return`DATEADD(DATETIME("${t}"), ${-Math.abs(l)}, ${n}) : ${t}`}return`DATEADD(DATETIME("${u}"), ${-Math.abs(l)}, ${n}) : DATEADD(DATETIME("${u}"), ${s}, ${r})`};var K=a(98286),P=a(35932),W=a(82342),j=a(37921),Q=a(76697),_=a(82191),B=a(70163),tt=a(81315),et=a(58593),at=a(69856),nt=a(12515),lt=a(27600),it=a(53350),ot=a(87183),rt=a(11965);function st(t){let e="Last week";return T.has(t.value)?e=t.value:t.onChange(e),(0,rt.tZ)(i.Fragment,null,(0,rt.tZ)("div",{className:"section-title"},(0,c.t)("Configure Time Range: Last...")),(0,rt.tZ)(ot.Y.Group,{value:e,onChange:e=>t.onChange(e.target.value)},b.map((({value:t,label:e})=>(0,rt.tZ)(ot.Y,{key:t,value:t,className:"vertical-radio"},e)))))}function ut({onChange:t,value:e}){return(0,i.useEffect)((()=>{M.has(e)||t(g)}),[t,e]),M.has(e)?(0,rt.tZ)(i.Fragment,null,(0,rt.tZ)("div",{className:"section-title"},(0,c.t)("Configure Time Range: Previous...")),(0,rt.tZ)(ot.Y.Group,{value:e,onChange:e=>t(e.target.value)},w.map((({value:t,label:e})=>(0,rt.tZ)(ot.Y,{key:t,value:t,className:"vertical-radio"},e))))):null}var ct=a(93754),dt=a.n(ct),mt=a(62276),pt=a(9882);const ht=(0,tt.m)("order");function Zt(t){const{customRange:e,matchedFlag:a}=J(t.value);a||t.onChange(H(e));const{sinceDatetime:n,sinceMode:l,sinceGrain:i,sinceGrainValue:o,untilDatetime:r,untilMode:s,untilGrain:u,untilGrainValue:d,anchorValue:m,anchorMode:p}={...e};function h(a,n){t.onChange(H({...e,[a]:n}))}function Z(a,n){dt()(n)&&n>0&&t.onChange(H({...e,[a]:n}))}return(0,rt.tZ)("div",null,(0,rt.tZ)("div",{className:"section-title"},(0,c.t)("Configure custom time range")),(0,rt.tZ)(_.X2,{gutter:24},(0,rt.tZ)(_.JX,{span:12},(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("START (INCLUSIVE)")," ",(0,rt.tZ)(pt.V,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})),(0,rt.tZ)(tt.Z,{ariaLabel:(0,c.t)("START (INCLUSIVE)"),options:S,value:l,onChange:t=>h("sinceMode",t),sortComparator:ht}),"specific"===l&&(0,rt.tZ)(_.X2,null,(0,rt.tZ)(mt.M,{showTime:!0,defaultValue:O(n),onChange:t=>h("sinceDatetime",t.format(A)),allowClear:!1})),"relative"===l&&(0,rt.tZ)(_.X2,{gutter:8},(0,rt.tZ)(_.JX,{span:11},(0,rt.tZ)(_.Rn,{placeholder:(0,c.t)("Relative quantity"),value:Math.abs(o),min:1,defaultValue:1,onChange:t=>Z("sinceGrainValue",t||1),onStep:t=>Z("sinceGrainValue",t||1)})),(0,rt.tZ)(_.JX,{span:13},(0,rt.tZ)(tt.Z,{ariaLabel:(0,c.t)("Relative period"),options:x,value:i,onChange:t=>h("sinceGrain",t),sortComparator:ht})))),(0,rt.tZ)(_.JX,{span:12},(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("END (EXCLUSIVE)")," ",(0,rt.tZ)(pt.V,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})),(0,rt.tZ)(tt.Z,{ariaLabel:(0,c.t)("END (EXCLUSIVE)"),options:$,value:s,onChange:t=>h("untilMode",t),sortComparator:ht}),"specific"===s&&(0,rt.tZ)(_.X2,null,(0,rt.tZ)(mt.M,{showTime:!0,defaultValue:O(r),onChange:t=>h("untilDatetime",t.format(A)),allowClear:!1})),"relative"===s&&(0,rt.tZ)(_.X2,{gutter:8},(0,rt.tZ)(_.JX,{span:11},(0,rt.tZ)(_.Rn,{placeholder:(0,c.t)("Relative quantity"),value:d,min:1,defaultValue:1,onChange:t=>Z("untilGrainValue",t||1),onStep:t=>Z("untilGrainValue",t||1)})),(0,rt.tZ)(_.JX,{span:13},(0,rt.tZ)(tt.Z,{ariaLabel:(0,c.t)("Relative period"),options:N,value:u,onChange:t=>h("untilGrain",t),sortComparator:ht}))))),"relative"===l&&"relative"===s&&(0,rt.tZ)("div",{className:"control-anchor-to"},(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("Anchor to")),(0,rt.tZ)(_.X2,{align:"middle"},(0,rt.tZ)(_.JX,null,(0,rt.tZ)(ot.Y.Group,{onChange:function(a){const n=a.target.value;"now"===n?t.onChange(H({...e,anchorValue:"now",anchorMode:n})):t.onChange(H({...e,anchorValue:k,anchorMode:n}))},defaultValue:"now",value:p},(0,rt.tZ)(ot.Y,{key:"now",value:"now"},(0,c.t)("NOW")),(0,rt.tZ)(ot.Y,{key:"specific",value:"specific"},(0,c.t)("Date/Time")))),"now"!==p&&(0,rt.tZ)(_.JX,null,(0,rt.tZ)(mt.M,{showTime:!0,defaultValue:O(m),onChange:t=>h("anchorValue",t.format(A)),allowClear:!1,className:"control-anchor-to-datetime"})))))}const gt=(0,rt.tZ)(i.Fragment,null,(0,rt.tZ)("div",null,(0,rt.tZ)("h3",null,"DATETIME"),(0,rt.tZ)("p",null,(0,c.t)("Return to specific datetime.")),(0,rt.tZ)("h4",null,(0,c.t)("Syntax")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,"datetime([string])")),(0,rt.tZ)("h4",null,(0,c.t)("Example")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,'datetime("2020-03-01 12:00:00")\ndatetime("now")\ndatetime("last year")'))),(0,rt.tZ)("div",null,(0,rt.tZ)("h3",null,"DATEADD"),(0,rt.tZ)("p",null,(0,c.t)("Moves the given set of dates by a specified interval.")),(0,rt.tZ)("h4",null,(0,c.t)("Syntax")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,"dateadd([datetime], [integer], [dateunit])\ndateunit = (year | quarter | month | week | day | hour | minute | second)")),(0,rt.tZ)("h4",null,(0,c.t)("Example")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,'dateadd(datetime("today"), -13, day)\ndateadd(datetime("2020-03-01"), 2, day)'))),(0,rt.tZ)("div",null,(0,rt.tZ)("h3",null,"DATETRUNC"),(0,rt.tZ)("p",null,(0,c.t)("Truncates the specified date to the accuracy specified by the date unit.")),(0,rt.tZ)("h4",null,(0,c.t)("Syntax")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,"datetrunc([datetime], [dateunit])\ndateunit = (year | quarter | month | week)")),(0,rt.tZ)("h4",null,(0,c.t)("Example")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,'datetrunc(datetime("2020-03-01"), week)\ndatetrunc(datetime("2020-03-01"), month)'))),(0,rt.tZ)("div",null,(0,rt.tZ)("h3",null,"LASTDAY"),(0,rt.tZ)("p",null,(0,c.t)("Get the last date by the date unit.")),(0,rt.tZ)("h4",null,(0,c.t)("Syntax")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,"lastday([datetime], [dateunit])\ndateunit = (year | month | week)")),(0,rt.tZ)("h4",null,(0,c.t)("Example")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,'lastday(datetime("today"), month)'))),(0,rt.tZ)("div",null,(0,rt.tZ)("h3",null,"HOLIDAY"),(0,rt.tZ)("p",null,(0,c.t)("Get the specify date for the holiday")),(0,rt.tZ)("h4",null,(0,c.t)("Syntax")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,"holiday([string])\nholiday([holiday string], [datetime])\nholiday([holiday string], [datetime], [country name])")),(0,rt.tZ)("h4",null,(0,c.t)("Example")),(0,rt.tZ)("pre",null,(0,rt.tZ)("code",null,'holiday("new year")\nholiday("christmas", datetime("2019"))\nholiday("christmas", dateadd(datetime("2019"), 1, year))\nholiday("christmas", datetime("2 years ago"))\nholiday("Easter Monday", datetime("2019"), "UK")')))),vt=t=>{const e=(0,u.Fg)();return(0,rt.tZ)(rt.ms,null,(({css:a})=>(0,rt.tZ)(et.u,l()({overlayClassName:a`
            .ant-tooltip-content {
              min-width: ${125*e.gridUnit}px;
              max-height: 410px;
              overflow-y: scroll;

              .ant-tooltip-inner {
                max-width: ${125*e.gridUnit}px;
                h3 {
                  font-size: ${e.typography.sizes.m}px;
                  font-weight: ${e.typography.weights.bold};
                }
                h4 {
                  font-size: ${e.typography.sizes.m}px;
                  font-weight: ${e.typography.weights.bold};
                }
                pre {
                  border: none;
                  text-align: left;
                  word-break: break-word;
                  font-size: ${e.typography.sizes.s}px;
                }
              }
            }
          `},t))))};function ft(t){return(0,rt.tZ)(vt,l()({title:gt},t))}function yt(t){const e=l(t.value||""),[a,n]=e.split(p);function l(t){return t.includes(p)?t:t.startsWith("Last")?[t,""].join(p):t.startsWith("Next")?["",t].join(p):p}function o(e,l){"since"===e?t.onChange(`${l} : ${n}`):t.onChange(`${a} : ${l}`)}return e!==t.value&&t.onChange(l(t.value||"")),(0,rt.tZ)(i.Fragment,null,(0,rt.tZ)("div",{className:"section-title"},(0,c.t)("Configure Advanced Time Range "),(0,rt.tZ)(ft,{placement:"rightBottom"},(0,rt.tZ)("i",{className:"fa fa-info-circle text-muted"}))),(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("START (INCLUSIVE)")," ",(0,rt.tZ)(pt.V,{tooltip:(0,c.t)("Start date included in time range"),placement:"right"})),(0,rt.tZ)(_.II,{key:"since",value:a,onChange:t=>o("since",t.target.value)}),(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("END (EXCLUSIVE)")," ",(0,rt.tZ)(pt.V,{tooltip:(0,c.t)("End date excluded from time range"),placement:"right"})),(0,rt.tZ)(_.II,{key:"until",value:n,onChange:t=>o("until",t.target.value)}))}const bt=async(t,e)=>{const a=`/api/v1/time_range/?q=${r().encode_uri(t)}`;try{var n,l,i,o;const t=await s.Z.get({endpoint:a}),r=`${(null==t||null==(n=t.json)||null==(l=n.result)?void 0:l.since)||""} : ${(null==t||null==(i=t.json)||null==(o=i.result)?void 0:o.until)||""}`;return{value:Z(r,e)}}catch(t){const e=await(0,K.O)(t);return{error:e.message||e.error}}},Ct=(0,u.iK)(Q.Z)``,wt=(0,u.iK)(tt.Z)`
  width: 272px;
`,Et=u.iK.div`
  .ant-row {
    margin-top: 8px;
  }

  .ant-input-number {
    width: 100%;
  }

  .ant-picker {
    padding: 4px 17px 4px;
    border-radius: 4px;
    width: 100%;
  }

  .ant-divider-horizontal {
    margin: 16px 0;
  }

  .control-label {
    font-size: 11px;
    font-weight: 500;
    color: #b2b2b2;
    line-height: 16px;
    text-transform: uppercase;
    margin: 8px 0;
  }

  .vertical-radio {
    display: block;
    height: 40px;
    line-height: 40px;
  }

  .section-title {
    font-style: normal;
    font-weight: 500;
    font-size: 15px;
    line-height: 24px;
    margin-bottom: 8px;
  }

  .control-anchor-to {
    margin-top: 16px;
  }

  .control-anchor-to-datetime {
    width: 217px;
  }

  .footer {
    text-align: right;
  }
`,Dt=u.iK.span`
  span {
    margin-right: ${({theme:t})=>2*t.gridUnit}px;
    vertical-align: middle;
  }
  .text {
    vertical-align: middle;
  }
  .error {
    color: ${({theme:t})=>t.colors.error.base};
  }
`,xt=(0,it.Q)("date-filter-control");function Nt(t){const{value:e=at.X5,endpoints:a,onChange:n,type:o}=t,[r,s]=(0,i.useState)(e),[d,m]=(0,i.useState)(!1),p=(0,i.useMemo)((()=>{return t=e,C.has(t)?"Common":E.has(t)?"Calendar":"No filter"===t?"No filter":J(t).matchedFlag?"Custom":"Advanced";var t}),[e]),[h,Z]=(0,i.useState)(p),[g,v]=(0,i.useState)(e),[f,b]=(0,i.useState)(e),[w,D]=(0,i.useState)(!1),[x,N]=(0,i.useState)(e),[S,$]=(0,i.useState)(e);function T(){b(e),Z(p),m(!1)}(0,i.useEffect)((()=>{bt(e,a).then((({value:t,error:a})=>{a?(N(a||""),D(!1),$(e||"")):("Common"===p||"Calendar"===p||"No filter"===p?(s(e),$("error"===o?(0,c.t)("Default value is required"):t||"")):(s(t||""),$(e||"")),D(!0)),v(e)}))}),[e]),(0,nt.bX)((()=>{g!==f&&bt(f,a).then((({value:t,error:e})=>{e?(N(e||""),D(!1)):(N(t||""),D(!0)),v(f)}))}),lt.M$,[f]);const M=(0,u.Fg)(),A=(0,rt.tZ)(Et,null,(0,rt.tZ)("div",{className:"control-label"},(0,c.t)("RANGE TYPE")),(0,rt.tZ)(wt,{ariaLabel:(0,c.t)("RANGE TYPE"),options:y,value:h,onChange:function(t){"No filter"===t&&b("No filter"),Z(t)},sortComparator:(0,tt.m)("order")}),"No filter"!==h&&(0,rt.tZ)(_.iz,null),"Common"===h&&(0,rt.tZ)(st,{value:f,onChange:b}),"Calendar"===h&&(0,rt.tZ)(ut,{value:f,onChange:b}),"Advanced"===h&&(0,rt.tZ)(yt,{value:f,onChange:b}),"Custom"===h&&(0,rt.tZ)(Zt,{value:f,onChange:b}),"No filter"===h&&(0,rt.tZ)("div",null),(0,rt.tZ)(_.iz,null),(0,rt.tZ)("div",null,(0,rt.tZ)("div",{className:"section-title"},(0,c.t)("Actual time range")),w&&(0,rt.tZ)("div",null,x),!w&&(0,rt.tZ)(Dt,{className:"warning"},(0,rt.tZ)(B.Z.ErrorSolidSmall,{iconColor:M.colors.error.base}),(0,rt.tZ)("span",{className:"text error"},x))),(0,rt.tZ)(_.iz,null),(0,rt.tZ)("div",{className:"footer"},(0,rt.tZ)(P.Z,{buttonStyle:"secondary",cta:!0,key:"cancel",onClick:T},(0,c.t)("CANCEL")),(0,rt.tZ)(P.Z,l()({buttonStyle:"primary",cta:!0,disabled:!w,key:"apply",onClick:function(){n(f),m(!1)}},xt("apply-button")),(0,c.t)("APPLY")))),V=(0,rt.tZ)(Dt,null,(0,rt.tZ)(B.Z.EditAlt,{iconColor:M.colors.grayscale.base}),(0,rt.tZ)("span",{className:"text"},(0,c.t)("Edit time range")));return(0,rt.tZ)(i.Fragment,null,(0,rt.tZ)(W.Z,t),(0,rt.tZ)(Ct,{placement:"right",trigger:"click",content:A,title:V,defaultVisible:d,visible:d,onVisibleChange:()=>{d?T():m(!0)},overlayStyle:{width:"600px"}},(0,rt.tZ)(et.u,{placement:"top",title:S},(0,rt.tZ)(j.Z,{className:"pointer",onClick:function(){b(e),Z(p),m(!0)}},r))))}},53350:(t,e,a)=>{a.d(e,{Q:()=>n});const n=(t,e=!1)=>(a,n=!1)=>{const l=n||e;if(!a&&t)return l?t:{"data-test":t};if(a&&!t)return l?a:{"data-test":a};if(!a&&!t)return console.warn('testWithId function has missed "prefix" and "id" params'),l?"":{"data-test":""};const i=`${t}__${a}`;return l?i:{"data-test":i}}}}]);