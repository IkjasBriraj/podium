import cv2
import base64
import httpx
import numpy as np
import os
import asyncio
import logging
from typing import List, Dict, Any, Tuple
from io import BytesIO
from PIL import Image

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class OllamaService:
    def __init__(self, model: str = "qwen2.5vl:latest", host: str = "http://localhost:11434"):
        self.model = model
        self.host = host
        self.api_url = f"{host}/api/generate"

    async def analyze_video(self, video_path: str, interval_seconds: int = 3) -> Dict[str, Any]:
        """
        Main entry point: Extracts frames from video and analyzes them using qwen2.5vl.
        Uses smart frame extraction to capture key moments.
        """
        logger.info(f"Starting analysis for video: {video_path}")
        
        # 1. Extract frames using motion detection for key moments
        frames = self._extract_smart_frames(video_path, interval_seconds)
        if not frames:
            return {
                "score": 0,
                "summary": "Could not extract frames from video.",
                "footworkScore": 0,
                "techniqueScore": 0,
                "positioningScore": 0,
                "tacticalScore": 0,
                "physicalScore": 0,
                "issues": []
            }
            
        logger.info(f"Extracted {len(frames)} key frames. Starting AI analysis...")

        # 2. Analyze frames concurrently
        tasks = []
        for i, frame_data in enumerate(frames):
            timestamp_str = frame_data["timestamp"]
            base64_img = frame_data["image"]
            motion_level = frame_data.get("motion_level", "medium")
            tasks.append(self._analyze_frame_enhanced(base64_img, timestamp_str, motion_level))
            
        # Run analysis in parallel (limit concurrency to avoid overloading GPU)
        chunk_size = 2  # Analyze 2 frames at a time for better GPU utilization
        results = []
        
        for i in range(0, len(tasks), chunk_size):
            chunk = tasks[i:i+chunk_size]
            chunk_results = await asyncio.gather(*chunk)
            results.extend(chunk_results)
            logger.info(f"Analyzed batch {i//chunk_size + 1}/{(len(tasks)+chunk_size-1)//chunk_size}")

        # 3. Aggregate results with enhanced scoring
        final_report = self._aggregate_results_enhanced(results)
        return final_report

    def _extract_smart_frames(self, video_path: str, interval: int) -> List[Dict[str, Any]]:
        """
        Extracts frames using motion detection to capture key action moments.
        Prioritizes frames with high motion (shot contact points).
        """
        frames = []
        cap = cv2.VideoCapture(video_path)
        
        if not cap.isOpened():
            logger.error("Error opening video file")
            return []

        fps = cap.get(cv2.CAP_PROP_FPS)
        if fps == 0:
            fps = 30  # Fallback
            
        frame_interval = int(fps * interval)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        
        prev_frame = None
        current_frame = 0
        motion_scores = []
        
        # First pass: Calculate motion scores for all interval frames
        candidate_frames = []
        
        while current_frame < total_frames:
            cap.set(cv2.CAP_PROP_POS_FRAMES, current_frame)
            ret, frame = cap.read()
            if not ret:
                break
            
            # Convert to grayscale for motion detection
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)
            
            motion_score = 0
            if prev_frame is not None:
                # Calculate frame difference for motion detection
                frame_diff = cv2.absdiff(prev_frame, gray)
                motion_score = np.mean(frame_diff)
            
            # Calculate timestamp with milliseconds for accuracy
            seconds = current_frame / fps
            minutes = int(seconds // 60)
            secs = int(seconds % 60)
            millis = int((seconds % 1) * 1000)
            timestamp_str = f"{minutes:02d}:{secs:02d}.{millis:03d}"
            
            # Preprocess frame for better analysis
            processed_frame = self._preprocess_frame(frame)
            
            # Encode frame to base64
            _, buffer = cv2.imencode('.jpg', processed_frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            base64_image = base64.b64encode(buffer).decode('utf-8')
            
            motion_level = "low"
            if motion_score > 15:
                motion_level = "high"
            elif motion_score > 8:
                motion_level = "medium"
            
            candidate_frames.append({
                "timestamp": timestamp_str,
                "image": base64_image,
                "motion_score": motion_score,
                "motion_level": motion_level,
                "frame_index": current_frame
            })
            
            prev_frame = gray
            current_frame += frame_interval

        cap.release()
        
        # Sort by motion score and select top frames (prioritize action moments)
        if len(candidate_frames) > 15:
            # Take mix of high-motion frames and evenly spaced frames
            sorted_by_motion = sorted(candidate_frames, key=lambda x: x["motion_score"], reverse=True)
            high_motion_frames = sorted_by_motion[:8]  # Top 8 high-motion frames
            
            # Add some evenly distributed frames for context
            step = len(candidate_frames) // 7
            distributed_frames = [candidate_frames[i] for i in range(0, len(candidate_frames), step)][:7]
            
            # Combine and remove duplicates
            selected = {f["frame_index"]: f for f in high_motion_frames + distributed_frames}
            frames = sorted(selected.values(), key=lambda x: x["frame_index"])
        else:
            frames = candidate_frames
        
        # Limit to 15 frames max
        return frames[:15]
    
    def _preprocess_frame(self, frame: np.ndarray) -> np.ndarray:
        """
        Preprocess frame for better AI analysis.
        - Normalize brightness/contrast
        - Resize to optimal dimensions
        """
        # Resize to reasonable dimensions for faster processing
        height, width = frame.shape[:2]
        max_dim = 1024  # Higher resolution for better analysis
        if max(height, width) > max_dim:
            scale = max_dim / max(height, width)
            frame = cv2.resize(frame, None, fx=scale, fy=scale, interpolation=cv2.INTER_AREA)
        
        # Apply CLAHE for better visibility
        lab = cv2.cvtColor(frame, cv2.COLOR_BGR2LAB)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8, 8))
        lab[:, :, 0] = clahe.apply(lab[:, :, 0])
        frame = cv2.cvtColor(lab, cv2.COLOR_LAB2BGR)
        
        return frame

    async def _analyze_frame_enhanced(self, base64_image: str, timestamp: str, motion_level: str) -> Dict[str, Any]:
        """
        Enhanced frame analysis with detailed badminton-specific prompting.
        Uses JSON output for reliable parsing.
        """
        # Simplified, focused prompt with JSON output requirement
        prompt = f"""You are an expert badminton coach analyzing a video frame at {timestamp}.

RULES:
1. ONLY analyze when a player is ABOUT TO HIT or IS HITTING the shuttlecock
2. If player is just receiving/waiting for shuttle, respond with: {{"skip": true}}
3. NEVER identify players by clothing color - colors are unreliable
4. Use ONLY these player identifiers:
   - "Near-side player" (closer to camera)
   - "Far-side player" (further from camera)  
   - "The player" (if only one visible)

If the player IS hitting/about to hit, analyze ONE of these categories:
- footwork: stance, split step, lunge, recovery
- technique: grip, swing, contact point, follow-through
- positioning: court coverage, base position
- tactical: shot selection, deception
- physical: balance, fatigue signs

Respond in this EXACT JSON format:
{{
  "title": "[Player ID]'s [Category]: [Brief Issue/Strength]",
  "player": "Near-side player" or "Far-side player" or "The player",
  "category": "footwork" or "technique" or "positioning" or "tactical" or "physical",
  "severity": "Critical" or "High" or "Medium" or "Low" or "Positive",
  "description": "Brief observation (1-2 sentences)",
  "recommendation": "Specific drill or practice tip",
  "confidence": "High" or "Medium" or "Low"
}}

Analyze this frame now:"""

        payload = {
            "model": self.model,
            "prompt": prompt,
            "images": [base64_image],
            "stream": False,
            "options": {
                "temperature": 0.2,  # Lower for more consistent JSON output
                "num_predict": 350,
                "top_p": 0.85
            }
        }

        try:
            async with httpx.AsyncClient(timeout=90.0) as client:
                response = await client.post(self.api_url, json=payload)
                response.raise_for_status()
                result = response.json()
                response_text = result.get("response", "")
                
                parsed = self._parse_enhanced_response(response_text, timestamp)
                return parsed
                
        except Exception as e:
            logger.error(f"Error analyzing frame at {timestamp}: {e}")
            return None

    def _parse_enhanced_response(self, text: str, timestamp: str) -> Dict[str, Any]:
        """
        Parse AI response - tries JSON first, then falls back to text parsing.
        Validates player identifiers to prevent color-based IDs.
        """
        import json
        import re
        
        # Valid player identifiers (no colors!)
        VALID_PLAYERS = ["Near-side player", "Far-side player", "The player"]
        VALID_CATEGORIES = ["footwork", "technique", "positioning", "tactical", "physical"]
        VALID_SEVERITIES = ["Critical", "High", "Medium", "Low", "Positive"]
        
        # Default fallback
        default_issue = {
            "title": "Analysis Inconclusive",
            "severity": "Low",
            "timestamp": timestamp,
            "description": "Could not clearly identify technique details in this frame.",
            "recommendation": "Review video quality or try different angles.",
            "category": "technique",
            "confidence": "Low",
            "player": "The player"
        }
        
        try:
            # Clean up response text
            text = text.strip()
            
            # Check if this is a skip response (player receiving, not hitting)
            if '"skip"' in text.lower() or "'skip'" in text.lower():
                logger.info(f"Frame at {timestamp}: Skipped (player receiving)")
                return None  # Will be filtered out
            
            # Try to extract JSON from the response
            json_match = re.search(r'\{[^{}]*\}', text, re.DOTALL)
            if json_match:
                try:
                    data = json.loads(json_match.group())
                    
                    # Check for skip signal
                    if data.get("skip"):
                        logger.info(f"Frame at {timestamp}: Skipped (player receiving)")
                        return None
                    
                    # Build issue from JSON data
                    issue = {
                        "timestamp": timestamp,
                        "title": str(data.get("title", "Observation"))[:80],
                        "description": str(data.get("description", ""))[:200],
                        "recommendation": str(data.get("recommendation", "Continue practicing"))[:200],
                        "confidence": "Medium"
                    }
                    
                    # Validate and set player (NO COLORS ALLOWED)
                    player = str(data.get("player", "The player"))
                    # Check if player contains any color - if so, default to position
                    color_words = ["red", "blue", "white", "black", "green", "yellow", "pink", "orange"]
                    if any(color in player.lower() for color in color_words):
                        # Extract position hint if available, otherwise default
                        if "near" in player.lower():
                            player = "Near-side player"
                        elif "far" in player.lower():
                            player = "Far-side player"
                        else:
                            player = "The player"
                    issue["player"] = player
                    
                    # Validate category
                    category = str(data.get("category", "technique")).lower()
                    if category in VALID_CATEGORIES:
                        issue["category"] = category
                    else:
                        # Try to infer from title/description
                        combined = (issue["title"] + " " + issue["description"]).lower()
                        if "foot" in combined or "step" in combined or "stance" in combined:
                            issue["category"] = "footwork"
                        elif "swing" in combined or "grip" in combined or "shot" in combined:
                            issue["category"] = "technique"
                        elif "position" in combined or "court" in combined:
                            issue["category"] = "positioning"
                        elif "tactic" in combined or "strateg" in combined:
                            issue["category"] = "tactical"
                        else:
                            issue["category"] = "technique"
                    
                    # Validate severity
                    severity = str(data.get("severity", "Medium"))
                    for valid_sev in VALID_SEVERITIES:
                        if valid_sev.lower() in severity.lower():
                            issue["severity"] = valid_sev
                            break
                    else:
                        issue["severity"] = "Medium"
                    
                    # Validate confidence
                    confidence = str(data.get("confidence", "Medium")).lower()
                    if "high" in confidence:
                        issue["confidence"] = "High"
                    elif "low" in confidence:
                        issue["confidence"] = "Low"
                    else:
                        issue["confidence"] = "Medium"
                    
                    logger.info(f"Frame at {timestamp}: Parsed JSON successfully - {issue['category']}")
                    return issue
                    
                except json.JSONDecodeError:
                    logger.debug(f"JSON parsing failed for frame at {timestamp}, falling back to text")
            
            # Fallback: Text-based parsing (simplified)
            text_clean = text.replace("**", "").replace("*", "").replace("#", "")
            lines = text_clean.strip().split('\n')
            
            issue = default_issue.copy()
            
            for line in lines:
                line_lower = line.lower().strip()
                
                # Extract key-value pairs
                if ':' in line:
                    key, _, value = line.partition(':')
                    key = key.strip().lower()
                    value = value.strip()
                    
                    if key in ["title", "issue", "finding"] and value:
                        issue["title"] = value[:80]
                    elif key == "description" and value:
                        issue["description"] = value[:200]
                    elif key == "recommendation" and value:
                        issue["recommendation"] = value[:200]
                    elif key == "severity":
                        for sev in VALID_SEVERITIES:
                            if sev.lower() in value.lower():
                                issue["severity"] = sev
                                break
                    elif key == "category":
                        for cat in VALID_CATEGORIES:
                            if cat in value.lower():
                                issue["category"] = cat
                                break
                    elif key == "player":
                        # Only accept position-based identifiers
                        if "near" in value.lower():
                            issue["player"] = "Near-side player"
                        elif "far" in value.lower():
                            issue["player"] = "Far-side player"
                        else:
                            issue["player"] = "The player"
            
            return issue
                
        except Exception as e:
            logger.error(f"Error parsing response at {timestamp}: {e}")
            return default_issue

    def _aggregate_results_enhanced(self, issues: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Enhanced aggregation with multi-category scoring and personalized recommendations.
        """
        valid_issues = [i for i in issues if i and i["title"] != "Analysis Inconclusive"]
        
        # Initialize category scores
        scores = {
            "footwork": {"base": 85, "count": 0},
            "technique": {"base": 85, "count": 0},
            "positioning": {"base": 85, "count": 0},
            "tactical": {"base": 85, "count": 0},
            "physical": {"base": 85, "count": 0}
        }
        
        # Deduction values based on severity
        deductions = {
            "Critical": 12,
            "High": 8,
            "Medium": 4,
            "Low": 2,
            "Positive": -3  # Bonus points
        }
        
        # Apply deductions/bonuses
        issue_categories = {}
        for issue in valid_issues:
            cat = issue.get("category", "technique")
            if cat not in scores:
                cat = "technique"
                
            val = deductions.get(issue["severity"], 0)
            scores[cat]["base"] -= val
            scores[cat]["count"] += 1
            
            # Track issues by category for recommendations
            if cat not in issue_categories:
                issue_categories[cat] = []
            if issue["severity"] not in ["Positive", "Low"]:
                issue_categories[cat].append(issue)
        
        # Clamp scores
        def clamp_score(s):
            return max(45, min(98, s))
        
        footwork_score = clamp_score(scores["footwork"]["base"])
        technique_score = clamp_score(scores["technique"]["base"])
        positioning_score = clamp_score(scores["positioning"]["base"])
        tactical_score = clamp_score(scores["tactical"]["base"])
        physical_score = clamp_score(scores["physical"]["base"])
        
        # Calculate weighted overall score
        overall_score = int(
            footwork_score * 0.25 +
            technique_score * 0.25 +
            positioning_score * 0.20 +
            tactical_score * 0.15 +
            physical_score * 0.15
        )
        
        # Generate personalized summary and recommendations
        weak_areas = []
        if footwork_score < 70:
            weak_areas.append("footwork")
        if technique_score < 70:
            weak_areas.append("shot technique")
        if positioning_score < 70:
            weak_areas.append("court positioning")
        if tactical_score < 70:
            weak_areas.append("tactical awareness")
        if physical_score < 70:
            weak_areas.append("physical conditioning")
        
        # Build summary
        summary = f"Analyzed {len(valid_issues)} key moments across {len([f for f in issues if f])} frames. "
        
        if overall_score >= 85:
            summary += "Excellent overall performance with strong fundamentals. "
        elif overall_score >= 70:
            summary += "Good performance with some areas for improvement. "
        elif overall_score >= 55:
            summary += "Moderate performance - focused training recommended. "
        else:
            summary += "Several fundamental areas need attention. "
        
        if weak_areas:
            summary += f"Priority focus areas: {', '.join(weak_areas)}."
        else:
            summary += "Maintain current training regimen for continued improvement."
        
        # Find top recommendations based on most critical issues
        top_recommendations = []
        all_recs = []
        for cat, cat_issues in issue_categories.items():
            for iss in cat_issues:
                if iss.get("recommendation") and iss["severity"] in ["Critical", "High", "Medium"]:
                    all_recs.append({
                        "category": cat,
                        "issue": iss["title"],
                        "recommendation": iss["recommendation"],
                        "priority": 1 if iss["severity"] == "Critical" else (2 if iss["severity"] == "High" else 3)
                    })
        
        # Sort by priority and take top 3
        all_recs.sort(key=lambda x: x["priority"])
        top_recommendations = all_recs[:3]

        return {
            "score": overall_score,
            "summary": summary,
            "footworkScore": footwork_score,
            "techniqueScore": technique_score,
            "positioningScore": positioning_score,
            "tacticalScore": tactical_score,
            "physicalScore": physical_score,
            "issues": valid_issues,
            "topRecommendations": top_recommendations,
            "framesAnalyzed": len([f for f in issues if f]),
            "issuesFound": len(valid_issues)
        }
