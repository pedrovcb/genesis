import React from 'react';

const Cadastro = ({ onCadastroSuccess }) => {
  return (
    <div className="med-step med-step--center">
      <h2>Tela de Cadastro</h2>
      <p>Página em construção...</p>
      <button className="med-btn med-btn--primary med-mt-16" onClick={onCadastroSuccess}>
        Simular Cadastro e Voltar
      </button>
    </div>
  );
};

export default Cadastro;