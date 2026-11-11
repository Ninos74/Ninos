// "Thirsty", a bouncy 12/8 pluck bed in C for the plant-scream reel. Original, written for this film.
import { line } from "/root/.claude/skills/synced/a0d1d366-d08d-4253-9b1e-083ba38422b6_c90de8ca-cc18-4cf9-bf0a-0b1dfddb64f5/take-one/scripts/music/plan.mjs";
const B = 4;
const rep = (s, n) => Array(n).fill(s).join(" ");
const bassBar = { C: "C3:1 G2:1 C3:1 G2:1", F: "F2:1 C3:1 F2:1 C3:1", G: "G2:1 D3:1 G2:1 D3:1", Am: "A2:1 E3:1 A2:1 E3:1" };
const compBar = { C: rep("r:2/3 [E4 G4]:1/3", 4), F: rep("r:2/3 [F4 A4]:1/3", 4), G: rep("r:2/3 [G4 B4]:1/3", 4), Am: rep("r:2/3 [C4 E4]:1/3", 4) };
const prog = ["C", "C", "F", "G", "C", "Am", "F", "G", "C", "C", "F", "G", "C", "Am", "F", "G"];
const m3 = "A5:2/3 C6:1/3 A5:2/3 F5:1/3 A5:1 r:1", m4 = "B5:2/3 D6:1/3 B5:2/3 G5:1/3 D5:1 r:1";
const m5 = "E5:2/3 G5:1/3 C6:1 G5:2/3 E5:1/3 C5:1", m6 = "E5:2/3 A5:1/3 C6:1 A5:2/3 E5:1/3 C5:1", m7 = "F5:2/3 A5:1/3 C6:1 A5:1 F5:1";
const mel = ["r:4", "r:4", m3, m4, m5, m6, m7, "G5:2/3 B5:1/3 D6:1 B5:1 r:1",
  "C6:1 G5:1 E5:1 G5:1", "C6:2/3 B5:1/3 A5:2/3 G5:1/3 E5:1 r:1", m3, m4, m5, m6, m7, "G5:1 B5:1 D6:1 G5:1", "C6:4"];
export default () => ({
  title: "Thirsty (bed in C)", seed: 707, tail: 1.6,
  harmony: [...prog, "C"].map((name, i) => ({ t: i * 4, name })),
  plan: { style: "musicBox", tempo: 118, meter: "12/8", phraseBars: 4,
    sections: [
      { id: "a", bars: 8, mood: "playful", key: "C", mode: "major", melody: ["hook"], dyn: [0.5, 0.62] },
      { id: "b", bars: 9, mood: "playful", key: "C", mode: "major", melody: ["hook"], dyn: [0.6, 0.5], ending: "tail" },
    ] },
  parts: [
    { id: "mel", inst: "musicBox", role: "melody", notes: line(0, mel.join(" | "), { role: "melody", v: 0.7, bpb: B }) },
    { id: "comp", inst: "softPluck", role: "accomp", gainDb: -5, notes: line(0, [...prog.map((c) => compBar[c]), "[E4 G4 C5]:4"].join(" | "), { role: "accomp", v: 0.55, bpb: B }) },
    { id: "bass", inst: "harp", role: "bass", notes: line(0, [...prog.map((c) => bassBar[c]), "[C2 G2 C3]:4"].join(" | "), { role: "bass", v: 0.7, bpb: B }) },
  ],
});
