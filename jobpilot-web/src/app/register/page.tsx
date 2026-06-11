"use client";
import { useState } from "react";
import axios from "axios";

export default function RegisterPage() {
  const [formData, setFormData] = useState({ nome: "", email: "", senha: "" });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      const response = await axios.post("http://localhost:8000/api/auth/registrar", formData);
      alert("Conta criada com sucesso! Redirecionando para login...");
      console.log(response.data);
    } catch (error: any) {
      alert(error.response?.data?.detail || "Erro ao criar conta");
    }
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 dark:bg-black">
      <form onSubmit={handleSubmit} className="w-full max-w-sm p-8 bg-white dark:bg-zinc-900 rounded-2xl border border-zinc-200 dark:border-zinc-800">
        <h2 className="text-2xl font-bold mb-6 text-black dark:text-white">Criar Conta</h2>
        <input 
          className="w-full p-3 mb-4 rounded-lg border border-zinc-300 dark:bg-black"
          placeholder="Nome" 
          onChange={(e) => setFormData({...formData, nome: e.target.value})} 
        />
        <input 
          className="w-full p-3 mb-4 rounded-lg border border-zinc-300 dark:bg-black"
          placeholder="E-mail" 
          type="email"
          onChange={(e) => setFormData({...formData, email: e.target.value})} 
        />
        <input 
          className="w-full p-3 mb-6 rounded-lg border border-zinc-300 dark:bg-black"
          placeholder="Senha" 
          type="password"
          onChange={(e) => setFormData({...formData, senha: e.target.value})} 
        />
        <button className="w-full py-3 bg-indigo-600 text-white rounded-full font-semibold hover:bg-indigo-700 transition">
          Registrar
        </button>
      </form>
    </div>
  );
}