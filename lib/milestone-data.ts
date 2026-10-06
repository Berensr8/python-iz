import raw from "@/content/milestones.json";
import type { MilestoneData } from "./milestones";

// Loaded through the bundler; Node scripts read the same JSON file directly.
export const milestones = raw as unknown as MilestoneData;
export const exams = milestones.exams;
export const workshops = milestones.workshops;
