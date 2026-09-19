<template>
  <div class="home">
    <section class="hero">
      <div class="grid-bg"></div>
      <div class="glow glow-one"></div>
      <div class="glow glow-two"></div>
      <div class="flight-path">
        <span class="path-dot"></span>
      </div>
      <div class="plane" @click="$router.push('/planner')" @mousemove="planeMove" @mouseleave="planeReset">✈</div>

      <div class="hero-text">
        <div class="eyebrow"><span></span> AI POWERED TRAVEL PLANNER <span></span></div>
        <p class="subtitle">AI · RAG · SMART TRAVEL</p>
        <h1>发现下一段<br><span>值得奔赴的旅程</span></h1>
        <p class="desc">基于真实旅行资料和 AI 技术，<br>为你生成有依据、可执行的个性化旅行计划。</p>
        <div class="hero-actions">
          <button class="primary-btn" @click="$router.push('/planner')">开始规划我的旅程 <span>→</span></button>
          <div class="hero-tip"><span class="tip-icon">✦</span> 基于 RAG 知识库生成</div>
        </div>
      </div>

      <div class="carousel">
        <div class="carousel-label left-label">EXPLORE</div>
        <div class="carousel-label right-label">YOUR JOURNEY</div>
        <div v-for="(item,index) in places" :key="item.name" class="place-card" :class="getPosition(index)" @click="jump(index)" @mousemove="moveCard" @mouseleave="resetCard">
          <img :src="item.image" :alt="item.name">
          <div class="card-overlay"></div>
          <div class="card-shine"></div>
          <div class="card-info">
            <span class="card-index">0{{ index + 1 }}</span>
            <h3>{{ item.name }}</h3>
            <p>{{ item.city }}</p>
          </div>
        </div>
        <div class="carousel-dots">
          <span v-for="(_,index) in places" :key="index" :class="{ active: index === current }" @click.stop="jump(index)"></span>
        </div>
      </div>
      <div class="scroll-hint"><span>SCROLL TO EXPLORE</span><i>↓</i></div>
    </section>

    <section class="workflow">
      <div class="section-heading">
        <div class="section-tag"><span></span> HOW IT WORKS <span></span></div>
        <h2>从旅行资料到<span>完整方案</span></h2>
        <p>让 AI 帮你处理复杂的旅行规划工作，把时间留给真正的旅程。</p>
      </div>
      <div class="steps">
        <div class="step" @mouseenter="activeStep=0" @mouseleave="activeStep=-1" :class="{ highlighted: activeStep === 0 }">
          <div class="step-top"><span class="step-number">01</span><span class="step-icon">↥</span></div>
          <div class="step-line"></div>
          <h3>上传旅行资料</h3>
          <p>将目的地相关资料上传至知识库。</p>
          <span class="step-tech">PDF / DOCX / TXT</span>
        </div>
        <div class="connector"><span></span></div>
        <div class="step" @mouseenter="activeStep=1" @mouseleave="activeStep=-1" :class="{ highlighted: activeStep === 1 }">
          <div class="step-top"><span class="step-number">02</span><span class="step-icon">⌕</span></div>
          <div class="step-line"></div>
          <h3>RAG 知识检索</h3>
          <p>从旅行资料中检索与需求相关的信息。</p>
          <span class="step-tech">VECTOR SEARCH</span>
        </div>
        <div class="connector"><span></span></div>
        <div class="step" @mouseenter="activeStep=2" @mouseleave="activeStep=-1" :class="{ highlighted: activeStep === 2 }">
          <div class="step-top"><span class="step-number">03</span><span class="step-icon">✦</span></div>
          <div class="step-line"></div>
          <h3>AI 生成行程</h3>
          <p>结合你的偏好生成完整旅行计划。</p>
          <span class="step-tech">AI AGENT</span>
        </div>
      </div>
    </section>

    <section class="features">
      <div class="feature-content">
        <div class="section-tag"><span></span> BUILT FOR TRAVEL <span></span></div>
        <h2>每一个行程<br><span>都有资料依据</span></h2>
        <p>不是简单地让 AI 猜一个攻略，而是基于你提供的旅行资料进行知识检索，再生成个性化行程。</p>
        <div class="feature-list">
          <div><b>01</b><span>真实资料支撑</span></div>
          <div><b>02</b><span>RAG 精准检索</span></div>
          <div><b>03</b><span>个性化规划</span></div>
        </div>
      </div>
      <div class="feature-visual">
        <div class="orbit orbit-one"></div>
        <div class="orbit orbit-two"></div>
        <div class="visual-card">
          <div class="visual-header"><span></span><span></span><span></span></div>
          <div class="visual-content">
            <div class="visual-icon">✦</div>
            <div class="visual-lines"><i></i><i></i><i></i></div>
            <div class="visual-tag">RAG</div>
          </div>
        </div>
        <div class="floating-tag tag-one">📚 Knowledge</div>
        <div class="floating-tag tag-two">🤖 AI Agent</div>
        <div class="floating-tag tag-three">✓ Citations</div>
      </div>
    </section>

    <section class="cta">
      <div class="cta-glow"></div>
      <div class="cta-content">
        <div class="section-tag"><span></span> START YOUR JOURNEY <span></span></div>
        <h2>下一站，<span>由你决定。</span></h2>
        <p>告诉 AI 你的目的地和旅行偏好，剩下的交给它。</p>
        <button class="primary-btn cta-btn" @click="$router.push('/planner')">创建我的旅行计划 <span>→</span></button>
      </div>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from "vue"

const places = [
  { name: "上海", city: "SHANGHAI · CHINA", image: "/images/shanghai.jpg" },
  { name: "广州", city: "GUANGZHOU · CHINA", image: "/images/guangzhou.jpg" },
  { name: "北京", city: "BEIJING · CHINA", image: "/images/beijing.jpg" },
  { name: "深圳", city: "SHENZHEN · CHINA", image: "/images/shenzhen.jpg" },
  { name: "杭州", city: "HANGZHOU · CHINA", image: "/images/hangzhou.jpg" },
  { name: "南京", city: "NANJING · CHINA", image: "/images/nanjing.jpg" }
]

const current = ref(0)
const activeStep = ref(-1)

function getPosition(index) {
  let diff = index - current.value
  if (diff < 0) diff += places.length
  if (diff === 0) return "active"
  if (diff === 1) return "right1"
  if (diff === 2) return "right2"
  if (diff === places.length - 1) return "left1"
  if (diff === places.length - 2) return "left2"
  return "hidden"
}

function jump(index) {
  current.value = index
}

function moveCard(e) {
  const card = e.currentTarget
  const rect = card.getBoundingClientRect()
  const x = e.clientX - rect.left
  const y = e.clientY - rect.top
  const rotateY = (x - rect.width / 2) / 22
  const rotateX = -(y - rect.height / 2) / 22
  card.style.setProperty("--rotateX", `${rotateX}deg`)
  card.style.setProperty("--rotateY", `${rotateY}deg`)
}

function resetCard(e) {
  const card = e.currentTarget
  card.style.setProperty("--rotateX", "0deg")
  card.style.setProperty("--rotateY", "0deg")
}

function planeMove(e) {
  const plane = e.currentTarget
  const rect = plane.getBoundingClientRect()
  const x = (e.clientX - rect.left - rect.width / 2) / 8
  const y = (e.clientY - rect.top - rect.height / 2) / 8
  plane.style.setProperty("--plane-x", `${x}px`)
  plane.style.setProperty("--plane-y", `${y}px`)
}

function planeReset(e) {
  e.currentTarget.style.setProperty("--plane-x", "0px")
  e.currentTarget.style.setProperty("--plane-y", "0px")
}

let timer

onMounted(() => {
  timer = setInterval(() => {
    current.value = (current.value + 1) % places.length
  }, 3000)
})

onUnmounted(() => {
  clearInterval(timer)
})
</script>

<style scoped>
.home{min-height:100vh;background:#faf8f3;color:#20252b;overflow:hidden;font-family:Inter,"PingFang SC","Microsoft YaHei",sans-serif}
.hero{min-height:1000px;position:relative;display:flex;flex-direction:column;align-items:center;padding-top:105px;background:linear-gradient(180deg,#faf8f3 0%,#fdfcf9 70%,#fff 100%);overflow:hidden}
.grid-bg{position:absolute;inset:0;opacity:.28;background-image:linear-gradient(rgba(217,130,91,.055) 1px,transparent 1px),linear-gradient(90deg,rgba(217,130,91,.055) 1px,transparent 1px);background-size:60px 60px;mask-image:linear-gradient(to bottom,#000,transparent 75%);pointer-events:none}
.glow{position:absolute;border-radius:50%;filter:blur(80px);pointer-events:none;animation:float 8s ease-in-out infinite alternate}
.glow-one{width:400px;height:400px;background:#f4c7a5;top:60px;right:8%;opacity:.28}
.glow-two{width:360px;height:360px;background:#ffd9a8;bottom:140px;left:4%;opacity:.22;animation-delay:-3s}
@keyframes float{from{transform:translateY(0) scale(1)}to{transform:translateY(35px) scale(1.05)}}
.hero-text{position:relative;z-index:5;text-align:center;animation:heroIn 1s ease-out}
@keyframes heroIn{from{opacity:0;transform:translateY(25px)}to{opacity:1;transform:translateY(0)}}
.eyebrow{display:flex;align-items:center;justify-content:center;gap:12px;color:#b8a99d;font-size:10px;letter-spacing:.28em}
.eyebrow span{width:25px;height:1px;background:#d9825b;opacity:.55}
.subtitle{margin:18px 0 0;color:#d9825b;font-size:12px;letter-spacing:.32em;font-weight:600}
h1{margin:22px 0 24px;font-size:78px;line-height:1.12;letter-spacing:-.055em;font-weight:800}
h1 span{background:linear-gradient(100deg,#c86f4d,#e9a16f 55%,#d9825b);-webkit-background-clip:text;background-clip:text;color:transparent}
.desc{margin:0;color:#747b84;font-size:16px;line-height:1.9}
.hero-actions{display:flex;flex-direction:column;align-items:center}
.primary-btn{display:inline-flex;align-items:center;justify-content:center;gap:22px;margin-top:32px;padding:15px 25px 15px 30px;border:1px solid rgba(255,255,255,.3);border-radius:50px;background:linear-gradient(135deg,#d9825b,#c96f4c);color:#fff;font-size:14px;font-weight:600;cursor:pointer;box-shadow:0 12px 30px rgba(201,111,76,.22);transition:.3s}
.primary-btn span{font-size:20px;line-height:1;transition:transform .3s}
.primary-btn:hover{transform:translateY(-4px);box-shadow:0 18px 40px rgba(201,111,76,.3)}
.primary-btn:hover span{transform:translateX(5px)}
.hero-tip{margin-top:14px;color:#a7a19b;font-size:10px;letter-spacing:.03em}
.tip-icon{color:#d9825b;margin-right:5px}
.flight-path{position:absolute;z-index:2;left:-10%;top:385px;width:120%;height:180px;border-top:1px dashed rgba(217,130,91,.22);border-radius:50%;transform:rotate(-9deg);pointer-events:none}
.flight-path:after{content:"";position:absolute;right:12%;top:-3px;width:6px;height:6px;border-radius:50%;background:#d9825b;box-shadow:0 0 0 5px rgba(217,130,91,.08),0 0 18px rgba(217,130,91,.35)}
.plane{position:absolute;z-index:7;left:-90px;top:420px;color:#d9825b;font-size:46px;cursor:pointer;filter:drop-shadow(0 12px 12px rgba(201,111,76,.2));transform:translate(var(--plane-x,0),var(--plane-y,0)) rotate(-15deg);animation:fly 9s cubic-bezier(.45,.05,.55,.95) infinite,floatPlane 2s ease-in-out infinite;transition:filter .25s,font-size .25s}
.plane:hover{font-size:54px;filter:drop-shadow(0 15px 20px rgba(201,111,76,.35))}
@keyframes fly{0%{left:-100px;top:500px;opacity:0}8%{opacity:1}48%{left:48%;top:330px}90%{opacity:1}100%{left:110%;top:135px;opacity:0}}
@keyframes floatPlane{0%,100%{margin-top:0}50%{margin-top:-8px}}
.carousel{position:relative;z-index:4;width:1200px;height:440px;margin-top:70px;display:flex;justify-content:center;align-items:center;perspective:1200px}
.carousel-label{position:absolute;top:205px;color:#c9c1ba;font-size:9px;letter-spacing:.3em;writing-mode:vertical-rl}
.left-label{left:20px}.right-label{right:20px}
.place-card{position:absolute;width:270px;height:370px;border-radius:26px;overflow:hidden;cursor:pointer;transform:translate(var(--tx,0)) rotateX(var(--rotateX,0deg)) rotateY(var(--rotateY,0deg)) scale(var(--scale,1));transition:transform .8s cubic-bezier(.2,1,.3,1),opacity .8s,box-shadow .4s;box-shadow:0 25px 60px rgba(40,30,20,.16);background:#ddd}
.place-card img{width:100%;height:100%;object-fit:cover;transition:transform .8s}
.place-card:hover img{transform:scale(1.07)}
.card-overlay{position:absolute;inset:0;background:linear-gradient(180deg,transparent 35%,rgba(15,12,10,.78) 100%)}
.card-shine{position:absolute;inset:0;background:linear-gradient(115deg,transparent 30%,rgba(255,255,255,.15) 50%,transparent 70%);transform:translateX(-120%);transition:transform .7s}
.place-card:hover .card-shine{transform:translateX(120%)}
.card-info{position:absolute;left:24px;right:24px;bottom:22px;color:#fff}
.card-index{display:block;margin-bottom:4px;color:rgba(255,255,255,.65);font-size:9px;letter-spacing:.18em}
.card-info h3{margin:0;font-size:34px;line-height:1.1;font-weight:700}
.card-info p{margin:7px 0 0;color:rgba(255,255,255,.7);font-size:9px;letter-spacing:.12em}
.active{--scale:1.08;z-index:10;box-shadow:0 35px 80px rgba(40,30,20,.22)}
.right1{--tx:285px;--scale:.9;opacity:.88;z-index:8}
.right2{--tx:500px;--scale:.76;opacity:.45;z-index:5}
.left1{--tx:-285px;--scale:.9;opacity:.88;z-index:8}
.left2{--tx:-500px;--scale:.76;opacity:.45;z-index:5}
.hidden{opacity:0;pointer-events:none}
.carousel-dots{position:absolute;bottom:-4px;display:flex;gap:7px}
.carousel-dots span{width:5px;height:5px;border-radius:50%;background:#d9d2cc;cursor:pointer;transition:.3s}
.carousel-dots span.active{width:20px;border-radius:5px;background:#d9825b}
.scroll-hint{position:absolute;bottom:25px;display:flex;flex-direction:column;align-items:center;gap:6px;color:#bbb2aa;font-size:8px;letter-spacing:.25em}
.scroll-hint i{font-size:16px;font-style:normal;animation:scrollDown 1.6s infinite}
@keyframes scrollDown{0%,100%{transform:translateY(0);opacity:.45}50%{transform:translateY(5px);opacity:1}}
.workflow{padding:125px 60px;background:#fff;text-align:center}
.section-heading{max-width:700px;margin:0 auto}
.section-tag{display:flex;align-items:center;justify-content:center;gap:10px;color:#d9825b;font-size:9px;font-weight:600;letter-spacing:.28em}
.section-tag span{width:22px;height:1px;background:#d9825b;opacity:.55}
.section-heading h2{margin:18px 0 12px;font-size:40px;letter-spacing:-.04em}
.section-heading h2 span{color:#d9825b}
.section-heading p{margin:0;color:#9298a0;font-size:13px;line-height:1.8}
.steps{max-width:1050px;margin:65px auto 0;display:flex;align-items:center;justify-content:center}
.step{position:relative;width:270px;min-height:230px;padding:28px;border:1px solid #eee9e4;border-radius:20px;background:#fff;text-align:left;box-shadow:0 12px 35px rgba(30,25,20,.045);transition:.35s}
.step:hover,.step.highlighted{transform:translateY(-8px);border-color:#e7c4b3;box-shadow:0 20px 45px rgba(180,110,80,.12)}
.step-top{display:flex;align-items:center;justify-content:space-between}
.step-number{color:#d9825b;font-size:25px;font-weight:700}
.step-icon{width:38px;height:38px;display:flex;align-items:center;justify-content:center;border-radius:11px;background:#faf0ea;color:#d9825b;font-size:17px}
.step-line{width:100%;height:1px;margin:20px 0;background:#eee9e4}
.step h3{margin:0 0 8px;font-size:17px}
.step p{margin:0;color:#8b929a;font-size:12px;line-height:1.7}
.step-tech{display:inline-block;margin-top:20px;padding:5px 8px;border-radius:5px;background:#f8f6f3;color:#b0a79f;font-size:8px;letter-spacing:.12em}
.connector{position:relative;width:70px;height:1px;background:#e5ded8}
.connector span{position:absolute;left:0;top:-2px;width:5px;height:5px;border-radius:50%;background:#d9825b;animation:connectorMove 2.5s linear infinite}
@keyframes connectorMove{0%{left:0;opacity:0}20%{opacity:1}80%{opacity:1}100%{left:100%;opacity:0}}
.features{min-height:600px;padding:120px 12%;display:flex;align-items:center;justify-content:space-between;gap:80px;background:#f7f4ef;overflow:hidden}
.feature-content{width:45%}
.feature-content .section-tag{justify-content:flex-start}
.feature-content h2{margin:20px 0;font-size:48px;line-height:1.2;letter-spacing:-.045em}
.feature-content h2 span{color:#d9825b}
.feature-content>p{max-width:460px;color:#777f87;font-size:14px;line-height:2}
.feature-list{margin-top:35px;border-top:1px solid #e4ddd5}
.feature-list div{display:flex;align-items:center;gap:22px;padding:15px 0;border-bottom:1px solid #e4ddd5}
.feature-list b{color:#d9825b;font-size:10px;letter-spacing:.1em}.feature-list span{font-size:13px;color:#555d65}
.feature-visual{position:relative;width:450px;height:390px;display:flex;align-items:center;justify-content:center}
.visual-card{position:relative;z-index:3;width:280px;height:205px;border:1px solid rgba(255,255,255,.8);border-radius:18px;background:rgba(255,255,255,.72);box-shadow:0 25px 70px rgba(100,75,50,.12);backdrop-filter:blur(15px);transform:rotate(-5deg);transition:.5s}
.visual-card:hover{transform:rotate(0) scale(1.04)}
.visual-header{height:35px;padding:0 14px;display:flex;align-items:center;gap:5px;border-bottom:1px solid #eee8e2}
.visual-header span{width:6px;height:6px;border-radius:50%;background:#d8cec5}
.visual-content{padding:30px;position:relative}.visual-icon{color:#d9825b;font-size:28px}.visual-lines{margin-top:15px}.visual-lines i{display:block;width:75%;height:5px;margin:7px 0;border-radius:5px;background:#e8e1da}.visual-lines i:nth-child(2){width:55%}.visual-lines i:nth-child(3){width:65%}
.visual-tag{position:absolute;right:25px;top:30px;padding:5px 8px;border-radius:5px;background:#faf0ea;color:#d9825b;font-size:8px;font-weight:600}
.orbit{position:absolute;border:1px dashed rgba(217,130,91,.22);border-radius:50%;animation:orbitSpin 18s linear infinite}
.orbit-one{width:330px;height:330px}.orbit-two{width:430px;height:250px;transform:rotate(30deg);animation-duration:25s}
@keyframes orbitSpin{to{transform:rotate(360deg)}}
.floating-tag{position:absolute;z-index:4;padding:9px 13px;border:1px solid rgba(255,255,255,.8);border-radius:9px;background:rgba(255,255,255,.8);box-shadow:0 10px 30px rgba(70,50,30,.08);color:#777068;font-size:9px;backdrop-filter:blur(8px);animation:tagFloat 4s ease-in-out infinite}
.tag-one{top:40px;left:10px}.tag-two{right:5px;top:110px;animation-delay:-1.3s}.tag-three{bottom:40px;left:55px;animation-delay:-2.4s}
@keyframes tagFloat{0%,100%{transform:translateY(0)}50%{transform:translateY(-8px)}}
.cta{position:relative;min-height:440px;padding:110px 30px;display:flex;align-items:center;justify-content:center;text-align:center;background:#292725;color:#fff;overflow:hidden}
.cta:before{content:"";position:absolute;inset:0;background:radial-gradient(circle at 50% 50%,rgba(217,130,91,.16),transparent 50%)}
.cta-glow{position:absolute;width:500px;height:500px;border-radius:50%;background:#d9825b;filter:blur(150px);opacity:.08}
.cta-content{position:relative;z-index:2}
.cta .section-tag{color:#dca083}.cta .section-tag span{background:#dca083}
.cta h2{margin:22px 0 12px;font-size:58px;letter-spacing:-.05em}
.cta h2 span{color:#e3a27f}
.cta p{margin:0;color:#aaa5a0;font-size:14px}
.cta-btn{margin-top:30px}
@media(max-width:1100px){
.hero{min-height:900px;padding-top:90px}h1{font-size:65px}.carousel{width:100%;height:400px}.right2,.left2{opacity:0}.features{padding:100px 7%}
}
@media(max-width:800px){
.hero{min-height:820px;padding-top:75px}.eyebrow{font-size:8px}.subtitle{font-size:10px}h1{font-size:48px}.desc{font-size:13px}.carousel{height:330px;margin-top:55px}.place-card{width:210px;height:290px}.right1{--tx:175px}.left1{--tx:-175px}.carousel-label{display:none}.active{--scale:1.05}.right2,.left2,.hidden{opacity:0}.scroll-hint{display:none}.workflow{padding:85px 25px}.section-heading h2{font-size:30px}.steps{flex-direction:column;gap:12px}.step{width:min(100%,340px)}.connector{width:1px;height:35px}.connector span{animation:connectorVertical 2.5s linear infinite}.features{padding:80px 25px;flex-direction:column}.feature-content{width:100%;text-align:center}.feature-content .section-tag{justify-content:center}.feature-content h2{font-size:38px}.feature-list{text-align:left}.feature-visual{width:100%;max-width:430px}.cta{min-height:360px;padding:80px 20px}.cta h2{font-size:40px}
}
@keyframes connectorVertical{0%{top:0;opacity:0}20%{opacity:1}80%{opacity:1}100%{top:100%;opacity:0}}
@media(max-width:500px){
.hero{min-height:760px}.hero-text{padding:0 20px}h1{font-size:42px}.primary-btn{padding:14px 21px 14px 24px}.flight-path{top:360px}.plane{top:430px;font-size:34px}.carousel{margin-top:45px;height:285px}.place-card{width:185px;height:255px}.right1{--tx:125px;--scale:.8}.left1{--tx:-125px;--scale:.8}.card-info h3{font-size:26px}.card-info p{font-size:7px}.features{min-height:auto}.feature-visual{height:330px}.visual-card{width:245px}.orbit-one{width:280px;height:280px}.orbit-two{width:330px;height:210px}.floating-tag{font-size:8px}.tag-one{left:0}.tag-two{right:0}.cta h2{font-size:34px}
}
@media(prefers-reduced-motion:reduce){
*,*::before,*::after{animation-duration:.01ms!important;animation-iteration-count:1!important;scroll-behavior:auto!important;transition-duration:.01ms!important}
}
</style>