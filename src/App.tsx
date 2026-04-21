import React from 'react';
import { 
  Bot, 
  Terminal, 
  Code, 
  CheckCircle, 
  Activity, 
  Cpu, 
  Box, 
  Database, 
  Zap, 
  Search,
  Eye,
  AlertCircle
} from 'lucide-react';

export default function App() {
  return (
    <div className="min-h-screen bg-[#0A0A0B] text-[#E0E0E0] p-6 flex flex-col font-sans border-8 border-[#1A1A1C]">
      {/* Header */}
      <header className="flex justify-between items-end border-b border-[#333336] pb-4 mb-6">
        <div className="flex flex-col">
          <span className="text-[10px] tracking-[0.2em] text-[#8E9299] uppercase font-bold">Coursework: CMP3103 / CMP9050</span>
          <h1 className="text-4xl font-light tracking-tight italic font-serif text-white">
            TidyBot <span className="text-[#5E626B] font-sans italic text-2xl">Mission Control</span>
          </h1>
        </div>
        <div className="flex gap-8 text-right">
          <div className="flex flex-col">
            <span className="text-[10px] text-[#8E9299] uppercase italic">Author</span>
            <span className="text-white font-mono text-sm tracking-tight">K. BYAMUKAMA</span>
          </div>
          <div className="flex flex-col">
            <span className="text-[10px] text-[#8E9299] uppercase italic">Build Status</span>
            <span className="text-emerald-400 font-mono text-sm">READY_FOR_DEPLOYMENT</span>
          </div>
        </div>
      </header>

      {/* Main Content Grid */}
      <main className="grid grid-cols-12 gap-6 flex-grow overflow-hidden">
        
        {/* Left column: Artifacts & Metrics */}
        <aside className="col-span-3 space-y-4 flex flex-col">
          <div className="bg-[#151619] p-4 border border-[#2A2B2E] rounded-sm">
            <h3 className="text-[11px] text-[#8E9299] uppercase mb-3 tracking-widest border-b border-[#2A2B2E] pb-1 font-bold">System Manifest</h3>
            <div className="space-y-3">
              {[
                { label: "ROS_DISTRO", value: "HUMBLE", color: "text-blue-400" },
                { label: "PLATFORM", value: "AGILEX LIMO", color: "text-white" },
                { label: "NODES", value: "TIDY_BOT_CORE", color: "text-emerald-400" }
              ].map((item, i) => (
                <div key={i} className="flex justify-between font-mono text-[10px]">
                  <span className="text-[#5E626B] uppercase tracking-tighter">{item.label}</span>
                  <span className={item.color}>{item.value}</span>
                </div>
              ))}
            </div>
          </div>

          <div className="bg-[#151619] p-4 border border-[#2A2B2E] rounded-sm flex-grow">
            <h3 className="text-[11px] text-[#8E9299] uppercase mb-3 tracking-widest border-b border-[#2A2B2E] pb-1 font-bold">Key Artifacts</h3>
            <ul className="space-y-4 mt-4">
              {[
                { title: "TidyBot Node", detail: "cmp3103_tidy_bot/tidy_bot_node.py", icon: Code, status: "READY" },
                { title: "Project Guide", detail: "README.md", icon: Database, status: "DOCS_OK" },
                { title: "Logic Prototype", detail: "dashboard_legacy/", icon: Activity, status: "ARCHIVED" }
              ].map((item, i) => (
                <li key={i} className="flex items-start gap-3 group cursor-default">
                  <div className="w-6 h-6 rounded-sm border border-[#2A2B2E] bg-black flex items-center justify-center shrink-0 group-hover:border-blue-500/50 transition-colors">
                    <item.icon className="w-3 h-3 text-[#5E626B] group-hover:text-blue-400" />
                  </div>
                  <div className="overflow-hidden">
                    <p className="text-xs font-bold leading-none mb-1">{item.title}</p>
                    <p className="text-[9px] text-[#8E9299] truncate italic">{item.detail}</p>
                  </div>
                </li>
              ))}
            </ul>
          </div>
        </aside>

        {/* Center column: Vision & Logic logs */}
        <section className="col-span-6 flex flex-col gap-4">
          <div className="relative bg-black border border-[#2A2B2E] flex-grow overflow-hidden flex items-center justify-center group">
            <div className="absolute top-4 left-4 z-10 bg-black/80 px-2 py-1 border border-white/10 text-[9px] font-mono tracking-tighter text-[#E0E0E0] backdrop-blur-sm">
              CAMERA: RGBD_FRONT_SENSOR_STABLE
            </div>
            
            <div className="w-full h-full bg-[#1A1A1D] flex flex-col items-center justify-center opacity-30 select-none">
              <Eye className="w-24 h-24 text-[#333] mb-4" />
              <p className="font-serif italic text-2xl text-[#333]">Simulation Feed Offline</p>
            </div>

            {/* Target acquisition markers simulation */}
            <div className="absolute inset-0 flex items-center justify-center pointer-events-none opacity-20 group-hover:opacity-40 transition-opacity">
              <div className="w-48 h-48 border border-emerald-500/50 rounded-full flex items-center justify-center border-dashed animate-[spin_20s_linear_infinite]" />
              <div className="absolute w-[1px] h-full bg-emerald-500/20" />
              <div className="absolute w-full h-[1px] bg-emerald-500/20" />
            </div>

            <div className="absolute bottom-8 right-8 flex gap-3">
              <div className="flex flex-col items-center gap-1">
                <div className="w-4 h-4 bg-red-600 rounded-sm shadow-[0_0_15px_rgba(220,38,38,0.4)]" />
                <span className="text-[8px] font-mono text-red-500/80 uppercase">Patch</span>
              </div>
              <div className="flex flex-col items-center gap-1">
                <div className="w-4 h-4 bg-blue-600 rounded-sm shadow-[0_0_15px_rgba(37,99,235,0.4)]" />
                <span className="text-[8px] font-mono text-blue-500/80 uppercase">Target</span>
              </div>
            </div>
          </div>

          <div className="h-44 bg-black border border-[#2A2B2E] p-4 font-mono text-[10px] text-[#72CC72]/90 overflow-hidden leading-relaxed relative">
            <div className="absolute top-2 right-2 flex items-center gap-1">
              <div className="w-1 h-1 bg-green-500 rounded-full animate-pulse" />
              <span className="text-[8px] text-green-500/50 uppercase">Live Stream</span>
            </div>
            <div className="space-y-1">
              <p>[INFO] [limo_base]: Robot handshake verified. Odometry active.</p>
              <p>[INFO] [depth_camera]: Feature extraction complete. HSV masks loaded.</p>
              <p className="text-amber-500/80">[WARN] [lidar_scan]: Corner reflection detected at 120deg.</p>
              <p className="text-blue-400">[INFO] [tidy_controller]: TARGET_ACQUIRED: Blue_Object_04</p>
              <p className="text-emerald-400">[INFO] [tidy_controller]: Initiating PUSH sequence...</p>
              <p>[INFO] [tidy_controller]: Moving to state: PUSHING_TO_PATCH_RED</p>
            </div>
          </div>
        </section>

        {/* Right column: LiDAR & Control Hub */}
        <aside className="col-span-3 space-y-4">
          <div className="bg-[#151619] p-4 border border-[#2A2B2E] rounded-sm h-full flex flex-col">
            <h3 className="text-[11px] text-[#8E9299] uppercase mb-3 tracking-widest border-b border-[#2A2B2E] pb-1 font-bold italic">Occupancy Grid</h3>
            
            <div className="flex-grow bg-black/60 rounded-sm border border-[#2A2B2E] relative m-2 flex items-center justify-center overflow-hidden">
              <div className="absolute inset-0 opacity-20" style={{ backgroundImage: 'radial-gradient(circle, #8E9299 1px, transparent 1px)', backgroundSize: '16px 16px' }} />
              
              <div className="w-36 h-36 border border-[#2A2B2E] rounded-full flex items-center justify-center relative">
                <div className="absolute inset-0 border border-emerald-500/10 rounded-full scale-75" />
                <div className="absolute inset-0 border border-emerald-500/5 rounded-full scale-50" />
                <div className="w-2 h-2 bg-blue-500 rounded-full shadow-[0_0_10px_rgba(59,130,246,0.6)] z-10" />
                <div className="absolute w-24 h-[1px] bg-emerald-500/40 rotate-[120deg] origin-center animate-[pulse_2s_infinite]" />
              </div>

              <div className="absolute top-2 right-2 text-[8px] font-mono text-[#5E626B] uppercase">Scan Range: 12.0m</div>
            </div>

            <div className="space-y-3 mt-6">
              <div className="flex flex-col gap-1 px-1">
                <span className="text-[9px] text-[#8E9299] uppercase italic">System Protocols</span>
                <div className="flex items-center gap-2">
                  <CheckCircle className="w-3 h-3 text-emerald-500" />
                  <span className="text-[10px] font-mono text-white/70 tracking-tighter">LEVEL_03_COMPLIANCE_VERIFIED</span>
                </div>
              </div>

              <div className="pt-2 space-y-2">
                <button className="w-full bg-[#E0E0E0] text-black font-bold text-[10px] uppercase py-3 tracking-[0.2em] hover:bg-white transition-all active:scale-[0.98] cursor-default">
                  Start Deployment
                </button>
                <button className="w-full bg-red-900/10 text-red-500 border border-red-900/30 font-bold text-[10px] uppercase py-3 tracking-[0.2em] hover:bg-red-900/20 transition-all cursor-default">
                  Terminate Mission
                </button>
              </div>
            </div>
          </div>
        </aside>

      </main>

      {/* Footer */}
      <footer className="mt-6 flex justify-between items-center text-[10px] text-[#5E626B] font-mono border-t border-[#333336] pt-4 italic">
        <div className="flex items-center gap-4">
          <span>PIPELINE: HSV_VISION_D3</span>
          <span className="text-[#333336]">|</span>
          <span>SENSORS: LASER_SCAN_2D</span>
          <span className="text-[#333336]">|</span>
          <span>LATENCY: 8ms</span>
        </div>
        <div className="flex items-center gap-2">
          <span>B-ID: TIDY_V3_AF09</span>
          <Zap className="w-3 h-3 text-emerald-500" />
          <span>AGILEX LIMO CONTROL HUB</span>
        </div>
      </footer>
    </div>
  );
}

