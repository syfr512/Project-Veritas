"use client";

import { useState } from "react";
import { Shield, AlertTriangle, FileText, UploadCloud, ChevronRight, Activity, Clock, PlusCircle } from "lucide-react";
import { Button } from "@/components/ui/button";
import { Card, CardContent, CardDescription, CardHeader, CardTitle, CardFooter } from "@/components/ui/card";
import { Badge } from "@/components/ui/badge";
import { Dialog, DialogContent, DialogDescription, DialogFooter, DialogHeader, DialogTitle, DialogTrigger } from "@/components/ui/dialog";
// Add useRouter hook
import { useRouter } from "next/navigation";
import { useEffect } from "react";

export default function Dashboard() {
  const router = useRouter();
  const [incidents, setIncidents] = useState<any[]>([]);

  useEffect(() => {
    fetch("http://localhost:8000/api/incidents/")
      .then(res => res.json())
      .then(data => setIncidents(data))
      .catch(console.error);
  }, []);

  const [loading, setLoading] = useState(false);
  const [file, setFile] = useState<File | null>(null);

  const handleUpload = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!file) return;
    
    setLoading(true);
    try {
      // 1. Create Incident
      const createRes = await fetch("http://localhost:8000/api/incidents/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ title: `Analysis: ${file.name}` })
      });
      const incident = await createRes.json();

      // 2. Upload file & analyze
      const formData = new FormData();
      formData.append("file", file);
      
      const analyzeRes = await fetch(`http://localhost:8000/api/incidents/${incident.id}/analyze_file`, {
        method: "POST",
        body: formData
      });
      
      if (analyzeRes.ok) {
        router.push(`/incidents/${incident.id}`);
      }
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-background text-foreground p-8 font-sans selection:bg-primary selection:text-primary-foreground">
      <div className="max-w-6xl mx-auto space-y-8">
        
        {/* Header Section */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-center border-b border-border pb-6">
          <div>
            <h1 className="text-4xl font-extrabold tracking-tight bg-gradient-to-r from-white to-gray-400 bg-clip-text text-transparent">Project Veritas</h1>
            <p className="text-muted-foreground mt-2 text-lg">AI-Powered Multimodal Digital Impersonation Detection</p>
          </div>
          <div className="mt-4 md:mt-0 flex gap-4">
            <Button variant="outline" className="gap-2 border-border/50 hover:bg-muted/50 transition-colors">
              <Activity className="h-4 w-4 text-emerald-400" />
              System Status: Secure
            </Button>
            <Dialog>
              <DialogTrigger className="inline-flex items-center justify-center rounded-md text-sm font-medium transition-colors focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-ring focus-visible:ring-offset-2 disabled:opacity-50 disabled:pointer-events-none ring-offset-background bg-primary text-primary-foreground hover:bg-primary/90 h-10 py-2 px-4 gap-2 shadow-[0_0_15px_rgba(255,50,50,0.5)]">
                  <PlusCircle className="h-4 w-4" />
                  New Investigation
              </DialogTrigger>
              <DialogContent className="sm:max-w-[425px] border-border bg-card">
                <DialogHeader>
                  <DialogTitle>Start New Investigation</DialogTitle>
                  <DialogDescription>
                    Upload suspected communications for analysis by the fusion engine.
                  </DialogDescription>
                </DialogHeader>
                <form onSubmit={handleUpload}>
                  <div className="grid gap-4 py-4">
                    <label className="flex flex-col items-center justify-center border-2 border-dashed border-border rounded-xl p-8 hover:border-primary/50 transition-colors cursor-pointer group bg-muted/20">
                      <UploadCloud className="h-10 w-10 text-muted-foreground mb-4 group-hover:text-primary transition-colors" />
                      <p className="text-sm font-medium">{file ? file.name : "Click to select a file"}</p>
                      <p className="text-xs text-muted-foreground mt-1">Supports .eml, .txt, .wav, .mp4</p>
                      <input type="file" className="hidden" onChange={(e) => setFile(e.target.files?.[0] || null)} />
                    </label>
                  </div>
                  <DialogFooter>
                    <Button type="submit" disabled={!file || loading} className="w-full">
                      {loading ? "Analyzing..." : "Upload & Analyze"}
                    </Button>
                  </DialogFooter>
                </form>
              </DialogContent>
            </Dialog>
          </div>
        </div>

        {/* Stats Row */}
        <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
          <Card className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-border transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Total Scans</CardTitle>
              <Shield className="h-4 w-4 text-blue-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">142</div>
              <p className="text-xs text-muted-foreground mt-1">+12% from last week</p>
            </CardContent>
          </Card>
          <Card className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-border transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">Active Alerts</CardTitle>
              <AlertTriangle className="h-4 w-4 text-yellow-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">17</div>
              <p className="text-xs text-muted-foreground mt-1">4 require attention</p>
            </CardContent>
          </Card>
          <Card className="bg-card/50 backdrop-blur-sm border-border/50 hover:border-border transition-colors">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-muted-foreground">High Risk</CardTitle>
              <Activity className="h-4 w-4 text-orange-400" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold">5</div>
              <p className="text-xs text-muted-foreground mt-1">Escalated to analysts</p>
            </CardContent>
          </Card>
          <Card className="bg-card/50 backdrop-blur-sm border-destructive/20 hover:border-destructive/50 transition-colors shadow-[0_0_15px_rgba(255,0,0,0.1)]">
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-destructive">Critical</CardTitle>
              <AlertTriangle className="h-4 w-4 text-destructive" />
            </CardHeader>
            <CardContent>
              <div className="text-3xl font-bold text-destructive">2</div>
              <p className="text-xs text-muted-foreground mt-1">Immediate action required</p>
            </CardContent>
          </Card>
        </div>

        {/* Recent Incidents */}
        <div>
          <h2 className="text-2xl font-bold mb-6 flex items-center gap-2">
            <Clock className="h-5 w-5 text-primary" />
            Recent Investigations
          </h2>
          <div className="grid grid-cols-1 gap-4">
            {incidents.map((incident) => (
              <Card key={incident.id} onClick={() => router.push('/incidents/' + incident.id)} className="bg-card/40 border-border/40 hover:bg-card/60 transition-all cursor-pointer group relative overflow-hidden">
                <div className={`absolute left-0 top-0 bottom-0 w-1 ${incident.severity === 'CRITICAL' ? 'bg-destructive' : incident.severity === 'HIGH' ? 'bg-orange-500' : 'bg-yellow-500'}`}></div>
                <CardContent className="p-6 flex flex-col md:flex-row items-start md:items-center justify-between gap-4 pl-8">
                  <div className="space-y-1 flex-1">
                    <div className="flex items-center gap-3">
                      <span className="font-mono text-sm text-muted-foreground">{incident.id}</span>
                      <Badge variant={incident.severity === 'CRITICAL' ? 'destructive' : 'secondary'} className="font-semibold tracking-wider text-[10px]">
                        {incident.severity}
                      </Badge>
                      <Badge variant="outline" className="text-xs border-border/50 text-muted-foreground bg-muted/20">
                        {incident.status}
                      </Badge>
                    </div>
                    <h3 className="font-semibold text-lg group-hover:text-primary transition-colors">{incident.title}</h3>
                    <div className="flex items-center text-xs text-muted-foreground gap-4">
                      <span className="flex items-center gap-1"><Clock className="h-3 w-3" /> {incident.created_at ? new Date(incident.created_at).toLocaleString() : 'Just now'}</span>
                      <span className="flex items-center gap-1"><FileText className="h-3 w-3" /> Multimodal Fusion</span>
                    </div>
                  </div>
                  <Button variant="ghost" className="opacity-0 group-hover:opacity-100 transition-opacity">
                    View Details <ChevronRight className="h-4 w-4 ml-1" />
                  </Button>
                </CardContent>
              </Card>
            ))}
          </div>
        </div>

      </div>
    </div>

  );
}
