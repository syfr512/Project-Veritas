"use client";

import { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { ArrowLeft, ShieldAlert, Cpu, Network, CheckCircle2, AlertTriangle, ShieldX } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Progress } from "@/components/ui/progress";
import { Tabs, TabsContent, TabsList, TabsTrigger } from "@/components/ui/tabs";

export default function IncidentDetail() {
  const params = useParams();
  const router = useRouter();
  
  const [incident, setIncident] = useState<any>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchIncident() {
      try {
        const res = await fetch(`http://localhost:8000/api/incidents/${params.id}`);
        if (res.ok) {
          const data = await res.json();
          setIncident(data);
        }
      } catch (err) {
        console.error(err);
      } finally {
        setLoading(false);
      }
    }
    fetchIncident();
  }, [params.id]);

  if (loading) {
    return <div className="p-8">Loading...</div>;
  }

  if (!incident) {
    return <div className="p-8">Incident not found</div>;
  }

  return (
    <div className="min-h-screen bg-background text-foreground p-8 font-sans selection:bg-primary selection:text-primary-foreground">
      <div className="max-w-6xl mx-auto space-y-6">
        
        {/* Header */}
        <div className="flex items-center gap-4 border-b border-border pb-6">
          <Button variant="ghost" size="icon" onClick={() => router.push('/')} className="hover:bg-muted">
            <ArrowLeft className="h-5 w-5" />
          </Button>
          <div className="flex-1">
            <div className="flex items-center gap-3">
              <h1 className="text-3xl font-extrabold tracking-tight">INC-{incident.id}</h1>
              <Badge variant={incident.severity === 'CRITICAL' ? 'destructive' : 'secondary'} className="font-semibold">{incident.severity}</Badge>
              <Badge variant="outline" className="border-border/50 text-muted-foreground">{incident.status}</Badge>
            </div>
            <p className="text-muted-foreground mt-1">{incident.title}</p>
          </div>
          <div className="text-right">
            <div className="text-4xl font-black text-destructive">{incident.risk_score} <span className="text-xl text-muted-foreground font-medium">/ 100</span></div>
            <div className="text-sm font-medium text-muted-foreground uppercase tracking-widest mt-1">Fusion Risk Score</div>
          </div>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          
          {/* Left Column: Evidence Fusion */}
          <div className="lg:col-span-1 space-y-6">
            <Card className="bg-card/30 border-border/40 backdrop-blur-md">
              <CardHeader>
                <CardTitle className="flex items-center gap-2 text-lg">
                  <Network className="h-5 w-5 text-primary" />
                  Multimodal Evidence
                </CardTitle>
                <CardDescription>Deterministic & ML signals</CardDescription>
              </CardHeader>
              <CardContent className="space-y-6">
                <div className="space-y-2">
                  <div className="flex justify-between text-sm font-medium">
                    <span>Email Intelligence</span>
                    <span className="text-yellow-500">{incident.evidence_summary?.email_risk || 0}%</span>
                  </div>
                  <Progress value={incident.evidence_summary?.email_risk || 0} className="h-2 bg-muted [&>div]:bg-yellow-500" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm font-medium">
                    <span>URL Intelligence</span>
                    <span className="text-orange-500">{incident.evidence_summary?.url_risk || 0}%</span>
                  </div>
                  <Progress value={incident.evidence_summary?.url_risk || 0} className="h-2 bg-muted [&>div]:bg-orange-500" />
                </div>
                <div className="space-y-2">
                  <div className="flex justify-between text-sm font-medium">
                    <span>Media Analysis</span>
                    <span className="text-destructive">{incident.evidence_summary?.audio_risk || 0}%</span>
                  </div>
                  <Progress value={incident.evidence_summary?.audio_risk || 0} className="h-2 bg-muted [&>div]:bg-destructive shadow-[0_0_10px_rgba(255,0,0,0.5)]" />
                </div>
              </CardContent>
            </Card>
            
            <Card className="bg-card/30 border-border/40 backdrop-blur-md">
              <CardHeader>
                <CardTitle className="text-lg">Indicators of Compromise</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-wrap gap-2">
                  {(incident.evidence_summary?.indicators || []).map((indicator: string, i: number) => (
                    <Badge key={i} variant="secondary" className="bg-muted/50 text-muted-foreground font-mono text-xs border border-border/50">
                      {indicator}
                    </Badge>
                  ))}
                </div>
              </CardContent>
            </Card>
          </div>

          {/* Right Column: AI Copilot & Response */}
          <div className="lg:col-span-2 space-y-6">
            <Card className="bg-card/40 border-primary/20 shadow-[0_0_30px_rgba(255,50,50,0.05)] relative overflow-hidden">
              <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-primary to-transparent opacity-50"></div>
              <CardHeader className="pb-4">
                <div className="flex justify-between items-start">
                  <div>
                    <CardTitle className="flex items-center gap-2 text-xl">
                      <Cpu className="h-5 w-5 text-primary" />
                      AI Security Copilot
                    </CardTitle>
                    <CardDescription className="mt-1">Evidence-backed synthesis and response plan</CardDescription>
                  </div>
                  <Badge variant="outline" className="font-mono bg-background/50 border-primary/30 text-primary">
                    ATT&CK {incident.mitre_mapping || "None"}
                  </Badge>
                </div>
              </CardHeader>
              <CardContent className="space-y-6">
                
                <div className="bg-background/50 rounded-lg p-5 border border-border/50">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground mb-2 flex items-center gap-2">
                    <ShieldAlert className="h-4 w-4 text-orange-400" />
                    Attack Classification
                  </h3>
                  <p className="text-lg font-semibold text-foreground">{incident.attack_type || "Unclassified"}</p>
                </div>

                <div className="space-y-2">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground">Explanation</h3>
                  <p className="text-muted-foreground leading-relaxed">
                    {incident.ai_explanation || "No AI explanation generated."}
                  </p>
                </div>

                <div className="space-y-3 pt-4 border-t border-border/50">
                  <h3 className="text-sm font-bold uppercase tracking-wider text-muted-foreground mb-3">Recommended Verification Workflow</h3>
                  {(incident.recommended_actions || []).map((action: string, i: number) => (
                    <div key={i} className="flex items-start gap-3 bg-muted/20 p-3 rounded-md border border-border/30 hover:border-primary/30 transition-colors">
                      <div className="mt-0.5">
                        <CheckCircle2 className="h-4 w-4 text-emerald-500" />
                      </div>
                      <p className="text-sm">{action}</p>
                    </div>
                  ))}
                </div>

              </CardContent>
              <CardFooter className="bg-muted/10 border-t border-border/30 pt-4 flex justify-between">
                 <Button variant="outline" className="border-border/50">Download PDF Report</Button>
                 <Button className="bg-primary text-primary-foreground">Acknowledge & Escalate</Button>
              </CardFooter>
            </Card>
          </div>

        </div>
      </div>
    </div>
  );
}
